#include "ptz/controller.hpp"

#include <algorithm>
#include <cmath>

namespace ptz {

Controller::Controller(Transport& transport, CameraRouter router, ControllerConfig config)
    : transport_(transport), router_(router), config_(config) {}

void Controller::start(Milliseconds now) {
    state_ = ControllerState::Booting;
    communication_status_ = CommunicationStatus::Unknown;
    motion_ = {};
    last_input_ms_ = now;
    last_motion_send_ms_ = now;
    response_pending_ = false;
    focus_pulse_active_ = false;
    store_held_ = false;
}

std::uint8_t Controller::scaled_speed(float magnitude, std::uint8_t maximum) {
    const auto scaled = static_cast<int>(std::ceil(std::clamp(std::fabs(magnitude), 0.0F, 1.0F) *
                                                   static_cast<float>(maximum)));
    return static_cast<std::uint8_t>(std::clamp(scaled, 1, static_cast<int>(maximum)));
}

bool Controller::same_pan_tilt(const Motion& left, const Motion& right) {
    return left.pan == right.pan && left.tilt == right.tilt &&
           left.pan_speed == right.pan_speed && left.tilt_speed == right.tilt_speed;
}

bool Controller::same_zoom(const Motion& left, const Motion& right) {
    return left.zoom == right.zoom && left.zoom_speed == right.zoom_speed;
}

CameraRoute Controller::selected_route() const {
    const auto route = router_.route(selected_camera_);
    return route.value_or(CameraRoute{});
}

CommandResult Controller::send_packet(const CameraRoute& route,
                                      const Packet& packet,
                                      Milliseconds now) {
    const auto result = transport_.send(route.transport_port, packet);
    if (!result.accepted) {
        ++diagnostics_.transport_errors;
        communication_status_ = CommunicationStatus::TransportError;
        state_ = ControllerState::TransportFault;
        return CommandResult::TransportError;
    }
    ++diagnostics_.packets_sent;
    if (config_.expect_responses) {
        response_pending_ = true;
        response_deadline_ms_ = now + config_.response_timeout_ms;
        communication_status_ = CommunicationStatus::AwaitingReply;
    } else {
        communication_status_ = CommunicationStatus::Unknown;
    }
    return CommandResult::Sent;
}

CommandResult Controller::apply_joystick(const JoystickState& joystick, Milliseconds now) {
    if (!joystick.valid) {
        if (state_ == ControllerState::Ready) {
            if (!safe_stop(now)) {
                return CommandResult::TransportError;
            }
            ++diagnostics_.input_timeouts;
        }
        state_ = ControllerState::InputLost;
        store_held_ = false;
        return CommandResult::Disabled;
    }

    last_input_ms_ = now;
    if (state_ == ControllerState::Booting || state_ == ControllerState::InputLost) {
        if (!joystick.neutral()) {
            return CommandResult::Disabled;
        }
        state_ = ControllerState::Ready;
        return CommandResult::NoChange;
    }
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }

    const auto route = selected_route();
    if (!route.enabled || !has_capability(route.capabilities, Capability::PanTilt)) {
        return CommandResult::Unsupported;
    }
    const auto profile = config_.speeds[static_cast<std::size_t>(speed_mode_)];
    Motion desired;
    desired.pan = joystick.pan < 0.0F   ? visca::PanDirection::Left
                  : joystick.pan > 0.0F ? visca::PanDirection::Right
                                        : visca::PanDirection::Stop;
    desired.tilt = joystick.tilt < 0.0F   ? visca::TiltDirection::Down
                   : joystick.tilt > 0.0F ? visca::TiltDirection::Up
                                          : visca::TiltDirection::Stop;
    desired.zoom = joystick.zoom < 0.0F   ? visca::ZoomDirection::Wide
                   : joystick.zoom > 0.0F ? visca::ZoomDirection::Tele
                                          : visca::ZoomDirection::Stop;
    desired.pan_speed = desired.pan == visca::PanDirection::Stop
                            ? 1U
                            : scaled_speed(joystick.pan, profile.pan_max);
    desired.tilt_speed = desired.tilt == visca::TiltDirection::Stop
                             ? 1U
                             : scaled_speed(joystick.tilt, profile.tilt_max);
    desired.zoom_speed = desired.zoom == visca::ZoomDirection::Stop
                             ? 0U
                             : scaled_speed(joystick.zoom, profile.zoom_max);

    bool sent = false;
    const bool refresh = static_cast<Milliseconds>(now - last_motion_send_ms_) >=
                         config_.movement_refresh_ms;
    if (!same_pan_tilt(desired, motion_) || (!desired.pan_tilt_stopped() && refresh)) {
        const auto packet = visca::pan_tilt_drive(route.visca_address,
                                                  desired.pan_speed,
                                                  desired.tilt_speed,
                                                  desired.pan,
                                                  desired.tilt,
                                                  config_.visca_limits);
        if (!packet) {
            return CommandResult::Invalid;
        }
        const auto result = send_packet(route, *packet, now);
        if (result != CommandResult::Sent) {
            return result;
        }
        motion_.pan = desired.pan;
        motion_.tilt = desired.tilt;
        motion_.pan_speed = desired.pan_speed;
        motion_.tilt_speed = desired.tilt_speed;
        sent = true;
    }

    if (!same_zoom(desired, motion_) || (!desired.zoom_stopped() && refresh)) {
        if (!has_capability(route.capabilities, Capability::Zoom)) {
            ++diagnostics_.unsupported_actions;
            return CommandResult::Unsupported;
        }
        const auto packet = visca::zoom(route.visca_address,
                                        desired.zoom,
                                        desired.zoom_speed,
                                        config_.visca_limits);
        if (!packet) {
            return CommandResult::Invalid;
        }
        const auto result = send_packet(route, *packet, now);
        if (result != CommandResult::Sent) {
            return result;
        }
        motion_.zoom = desired.zoom;
        motion_.zoom_speed = desired.zoom_speed;
        sent = true;
    }
    if (sent) {
        last_motion_send_ms_ = now;
    }
    return sent ? CommandResult::Sent : CommandResult::NoChange;
}

bool Controller::safe_stop(Milliseconds now) {
    const auto route = selected_route();
    bool attempted = false;
    if (!motion_.pan_tilt_stopped()) {
        attempted = true;
        const auto packet = visca::pan_tilt_drive(route.visca_address,
                                                  1U,
                                                  1U,
                                                  visca::PanDirection::Stop,
                                                  visca::TiltDirection::Stop,
                                                  config_.visca_limits);
        if (!packet || send_packet(route, *packet, now) != CommandResult::Sent) {
            return false;
        }
    }
    if (!motion_.zoom_stopped()) {
        attempted = true;
        const auto packet = visca::zoom(route.visca_address,
                                        visca::ZoomDirection::Stop,
                                        0U,
                                        config_.visca_limits);
        if (!packet || send_packet(route, *packet, now) != CommandResult::Sent) {
            return false;
        }
    }
    if (focus_pulse_active_) {
        attempted = true;
        const auto packet = visca::focus_drive(route.visca_address, visca::FocusDrive::Stop);
        if (!packet || send_packet(route, *packet, now) != CommandResult::Sent) {
            return false;
        }
        focus_pulse_active_ = false;
    }
    motion_ = {};
    if (attempted) {
        ++diagnostics_.safety_stops;
    }
    return true;
}

CommandResult Controller::select_camera(std::uint8_t logical_camera, Milliseconds now) {
    const auto new_route = router_.route(logical_camera);
    if (!new_route) {
        ++diagnostics_.rejected_routes;
        return CommandResult::Invalid;
    }
    if (logical_camera == selected_camera_) {
        return CommandResult::NoChange;
    }
    if (!safe_stop(now)) {
        return CommandResult::TransportError;
    }
    selected_camera_ = logical_camera;
    // Treat the new camera's focus state as unknown/safe-to-command. The first
    // manual focus step will explicitly request manual mode.
    autofocus_enabled_ = true;
    communication_status_ = CommunicationStatus::Unknown;
    response_pending_ = false;
    return CommandResult::NoChange;
}

CommandResult Controller::send_preset(std::uint8_t preset_number,
                                      bool store,
                                      Milliseconds now) {
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }
    const auto route = selected_route();
    if (!has_capability(route.capabilities, Capability::Presets)) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    const auto packet = visca::preset(route.visca_address,
                                      store ? visca::PresetOperation::Store
                                            : visca::PresetOperation::Recall,
                                      preset_number,
                                      config_.visca_limits);
    return packet ? send_packet(route, *packet, now) : CommandResult::Invalid;
}

CommandResult Controller::set_autofocus(bool automatic, Milliseconds now) {
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }
    const auto route = selected_route();
    if (!has_capability(route.capabilities, Capability::Focus)) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    const auto packet = visca::focus_mode(route.visca_address, automatic);
    if (!packet) {
        return CommandResult::Invalid;
    }
    const auto result = send_packet(route, *packet, now);
    if (result == CommandResult::Sent) {
        autofocus_enabled_ = automatic;
    }
    return result;
}

CommandResult Controller::handle_button(PanelButton button,
                                        InputEvent event,
                                        Milliseconds now) {
    if (button == PanelButton::Store) {
        if (event == InputEvent::Pressed) {
            store_held_ = true;
        } else if (event == InputEvent::Released) {
            store_held_ = false;
        }
        return CommandResult::NoChange;
    }
    if (event != InputEvent::Pressed) {
        return CommandResult::NoChange;
    }

    const auto value = static_cast<std::uint8_t>(button);
    if (value <= static_cast<std::uint8_t>(PanelButton::Camera10)) {
        return select_camera(static_cast<std::uint8_t>(value + 1U), now);
    }
    if (value >= static_cast<std::uint8_t>(PanelButton::Preset1) &&
        value <= static_cast<std::uint8_t>(PanelButton::Preset12)) {
        const auto preset_number = static_cast<std::uint8_t>(
            value - static_cast<std::uint8_t>(PanelButton::Preset1) + 1U);
        return send_preset(preset_number, store_held_, now);
    }
    if (button == PanelButton::SpeedSlow) {
        speed_mode_ = SpeedMode::Slow;
        return CommandResult::NoChange;
    }
    if (button == PanelButton::SpeedMedium) {
        speed_mode_ = SpeedMode::Medium;
        return CommandResult::NoChange;
    }
    if (button == PanelButton::SpeedFast) {
        speed_mode_ = SpeedMode::Fast;
        return CommandResult::NoChange;
    }
    if (button == PanelButton::AutoFocus) {
        return set_autofocus(!autofocus_enabled_, now);
    }
    if (button == PanelButton::AutoIris) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    return CommandResult::Invalid;
}

CommandResult Controller::focus_step(int direction, Milliseconds now) {
    if (direction == 0) {
        return CommandResult::NoChange;
    }
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }
    const auto route = selected_route();
    if (!has_capability(route.capabilities, Capability::Focus)) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    if (autofocus_enabled_) {
        const auto manual = set_autofocus(false, now);
        if (manual != CommandResult::Sent) {
            return manual;
        }
    }
    const auto packet = visca::focus_drive(
        route.visca_address, direction > 0 ? visca::FocusDrive::Far : visca::FocusDrive::Near);
    if (!packet) {
        return CommandResult::Invalid;
    }
    const auto result = send_packet(route, *packet, now);
    if (result == CommandResult::Sent) {
        focus_pulse_active_ = true;
        focus_stop_due_ms_ = now + config_.focus_pulse_ms;
    }
    return result;
}

CommandResult Controller::iris_step(int direction, Milliseconds now) {
    if (direction == 0) {
        return CommandResult::NoChange;
    }
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }
    const auto route = selected_route();
    if (!has_capability(route.capabilities, Capability::Iris)) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    const auto packet = visca::iris(
        route.visca_address, direction > 0 ? visca::IrisAction::Up : visca::IrisAction::Down);
    return packet ? send_packet(route, *packet, now) : CommandResult::Invalid;
}

CommandResult Controller::set_white_balance(visca::WhiteBalanceMode mode,
                                            Milliseconds now) {
    if (state_ != ControllerState::Ready) {
        return CommandResult::Disabled;
    }
    const auto route = selected_route();
    if (!has_capability(route.capabilities, Capability::WhiteBalance)) {
        ++diagnostics_.unsupported_actions;
        return CommandResult::Unsupported;
    }
    const auto packet = visca::white_balance(route.visca_address, mode);
    return packet ? send_packet(route, *packet, now) : CommandResult::Invalid;
}

void Controller::on_transport_bytes(std::uint8_t physical_port,
                                    const std::uint8_t* data,
                                    std::size_t size,
                                    Milliseconds /*now*/) {
    const auto route = selected_route();
    if (physical_port != route.transport_port) {
        ++diagnostics_.protocol_errors;
        return;
    }
    const auto response = visca::parse_response(data, size);
    if (!response.valid) {
        ++diagnostics_.protocol_errors;
        communication_status_ = CommunicationStatus::ProtocolError;
        return;
    }
    if (response.type == visca::ResponseType::Error) {
        ++diagnostics_.protocol_errors;
        response_pending_ = false;
        communication_status_ = CommunicationStatus::ProtocolError;
    } else if (response.type == visca::ResponseType::Completion) {
        response_pending_ = false;
        communication_status_ = CommunicationStatus::Online;
    } else if (response.type == visca::ResponseType::Ack) {
        communication_status_ = CommunicationStatus::Acknowledged;
    }
}

void Controller::tick(Milliseconds now) {
    if (state_ == ControllerState::Ready &&
        static_cast<Milliseconds>(now - last_input_ms_) >= config_.input_timeout_ms) {
        if (safe_stop(now)) {
            ++diagnostics_.input_timeouts;
            state_ = ControllerState::InputLost;
            store_held_ = false;
        }
    }

    if (focus_pulse_active_ && static_cast<std::int32_t>(now - focus_stop_due_ms_) >= 0) {
        const auto route = selected_route();
        const auto packet = visca::focus_drive(route.visca_address, visca::FocusDrive::Stop);
        if (packet && send_packet(route, *packet, now) == CommandResult::Sent) {
            focus_pulse_active_ = false;
        }
    }

    if (response_pending_ && static_cast<std::int32_t>(now - response_deadline_ms_) >= 0) {
        response_pending_ = false;
        ++diagnostics_.response_timeouts;
        communication_status_ = CommunicationStatus::TimedOut;
        if (state_ == ControllerState::Ready) {
            safe_stop(now);
            state_ = ControllerState::TransportFault;
        }
        // A best-effort stop being accepted by the local transport does not
        // prove that the unresponsive remote camera received it.
        response_pending_ = false;
        communication_status_ = CommunicationStatus::TimedOut;
    }
}

void Controller::shutdown(Milliseconds now) {
    safe_stop(now);
    store_held_ = false;
    state_ = ControllerState::ShuttingDown;
}

void Controller::reset_fault(Milliseconds now) {
    start(now);
}

std::array<bool, 13> Controller::led_state() const {
    std::array<bool, 13> leds{};
    if (selected_camera_ >= 1U && selected_camera_ <= 10U) {
        leds[selected_camera_ - 1U] = true;
    }
    leds[10U + static_cast<std::size_t>(speed_mode_)] = true;
    return leds;
}

}  // namespace ptz
