#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

#include "ptz/inputs.hpp"
#include "ptz/joystick.hpp"
#include "ptz/router.hpp"
#include "ptz/transport.hpp"
#include "ptz/types.hpp"
#include "ptz/visca.hpp"

namespace ptz {

enum class ControllerState : std::uint8_t {
    Booting,
    Ready,
    InputLost,
    TransportFault,
    ShuttingDown,
};

enum class CommandResult : std::uint8_t {
    Sent,
    NoChange,
    Disabled,
    Unsupported,
    Invalid,
    TransportError,
};

enum class CommunicationStatus : std::uint8_t {
    Unknown,
    AwaitingReply,
    Acknowledged,
    Online,
    TimedOut,
    ProtocolError,
    TransportError,
};

struct ControllerConfig {
    std::array<SpeedProfile, 3> speeds{
        SpeedProfile{0x04, 0x04, 0x02},
        SpeedProfile{0x09, 0x09, 0x04},
        SpeedProfile{0x12, 0x12, 0x07},
    };
    visca::Limits visca_limits{};
    Milliseconds input_timeout_ms{250};
    Milliseconds response_timeout_ms{500};
    Milliseconds movement_refresh_ms{100};
    Milliseconds focus_pulse_ms{80};
    bool expect_responses{true};
};

struct Diagnostics {
    std::uint32_t packets_sent{0};
    std::uint32_t transport_errors{0};
    std::uint32_t protocol_errors{0};
    std::uint32_t response_timeouts{0};
    std::uint32_t input_timeouts{0};
    std::uint32_t rejected_routes{0};
    std::uint32_t unsupported_actions{0};
    std::uint32_t safety_stops{0};
};

class Controller {
  public:
    Controller(Transport& transport,
               CameraRouter router = {},
               ControllerConfig config = {});

    void start(Milliseconds now);
    CommandResult apply_joystick(const JoystickState& joystick, Milliseconds now);
    CommandResult handle_button(PanelButton button, InputEvent event, Milliseconds now);
    CommandResult focus_step(int direction, Milliseconds now);
    CommandResult iris_step(int direction, Milliseconds now);
    CommandResult set_white_balance(visca::WhiteBalanceMode mode, Milliseconds now);
    void on_transport_bytes(std::uint8_t physical_port,
                            const std::uint8_t* data,
                            std::size_t size,
                            Milliseconds now);
    void tick(Milliseconds now);
    void shutdown(Milliseconds now);
    void reset_fault(Milliseconds now);

    ControllerState state() const { return state_; }
    CommunicationStatus communication_status() const { return communication_status_; }
    std::uint8_t selected_camera() const { return selected_camera_; }
    SpeedMode speed_mode() const { return speed_mode_; }
    bool store_held() const { return store_held_; }
    bool autofocus_enabled() const { return autofocus_enabled_; }
    const Diagnostics& diagnostics() const { return diagnostics_; }
    std::array<bool, 13> led_state() const;

  private:
    struct Motion {
        visca::PanDirection pan{visca::PanDirection::Stop};
        visca::TiltDirection tilt{visca::TiltDirection::Stop};
        visca::ZoomDirection zoom{visca::ZoomDirection::Stop};
        std::uint8_t pan_speed{1};
        std::uint8_t tilt_speed{1};
        std::uint8_t zoom_speed{0};

        bool pan_tilt_stopped() const {
            return pan == visca::PanDirection::Stop && tilt == visca::TiltDirection::Stop;
        }
        bool zoom_stopped() const { return zoom == visca::ZoomDirection::Stop; }
    };

    static std::uint8_t scaled_speed(float magnitude, std::uint8_t maximum);
    static bool same_pan_tilt(const Motion& left, const Motion& right);
    static bool same_zoom(const Motion& left, const Motion& right);
    CommandResult select_camera(std::uint8_t logical_camera, Milliseconds now);
    CommandResult send_preset(std::uint8_t preset, bool store, Milliseconds now);
    CommandResult set_autofocus(bool automatic, Milliseconds now);
    CommandResult send_packet(const CameraRoute& route,
                              const Packet& packet,
                              Milliseconds now);
    bool safe_stop(Milliseconds now);
    CameraRoute selected_route() const;

    Transport& transport_;
    CameraRouter router_;
    ControllerConfig config_;
    ControllerState state_{ControllerState::Booting};
    CommunicationStatus communication_status_{CommunicationStatus::Unknown};
    Diagnostics diagnostics_{};
    Motion motion_{};
    std::uint8_t selected_camera_{1};
    SpeedMode speed_mode_{SpeedMode::Medium};
    Milliseconds last_input_ms_{0};
    Milliseconds last_motion_send_ms_{0};
    Milliseconds response_deadline_ms_{0};
    Milliseconds focus_stop_due_ms_{0};
    bool response_pending_{false};
    bool focus_pulse_active_{false};
    bool store_held_{false};
    bool autofocus_enabled_{true};
};

}  // namespace ptz
