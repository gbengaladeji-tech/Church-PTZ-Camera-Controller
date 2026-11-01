#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <utility>
#include <vector>

#include "ptz/controller.hpp"
#include "ptz/inputs.hpp"
#include "ptz/joystick.hpp"
#include "ptz/nextion.hpp"
#include "ptz/router.hpp"
#include "ptz/transport.hpp"
#include "ptz/visca.hpp"

namespace {

int failures = 0;
int checks = 0;

#define CHECK(condition)                                                                       \
    do {                                                                                       \
        ++checks;                                                                              \
        if (!(condition)) {                                                                    \
            ++failures;                                                                        \
            std::cerr << __FILE__ << ':' << __LINE__ << " CHECK failed: " #condition << '\n'; \
        }                                                                                      \
    } while (false)

bool bytes_equal(const ptz::Packet& packet,
                 std::initializer_list<std::uint8_t> expected) {
    if (packet.size != expected.size()) {
        return false;
    }
    std::size_t index = 0;
    for (const auto value : expected) {
        if (packet.bytes[index++] != value) {
            return false;
        }
    }
    return true;
}

bool frame_starts_with(const ptz::nextion::Frame& frame, std::string_view expected) {
    if (frame.size < expected.size() + 3U) {
        return false;
    }
    for (std::size_t index = 0; index < expected.size(); ++index) {
        if (frame.bytes[index] != static_cast<std::uint8_t>(expected[index])) {
            return false;
        }
    }
    return frame.bytes[frame.size - 1U] == 0xFFU &&
           frame.bytes[frame.size - 2U] == 0xFFU &&
           frame.bytes[frame.size - 3U] == 0xFFU;
}

struct Transmission {
    std::uint8_t port;
    ptz::Packet packet;
};

class FakeTransport final : public ptz::Transport {
  public:
    ptz::SendResult send(std::uint8_t port, const ptz::Packet& packet) override {
        if (fail) {
            return {false, ptz::TransportError::Disconnected};
        }
        sent.push_back({port, packet});
        return {true, ptz::TransportError::None};
    }

    bool fail{false};
    std::vector<Transmission> sent;
};

void test_visca_packets() {
    using namespace ptz::visca;
    const auto move = pan_tilt_drive(3, 0x04, 0x09, PanDirection::Left, TiltDirection::Up);
    CHECK(move.has_value());
    CHECK(bytes_equal(*move, {0x83, 0x01, 0x06, 0x01, 0x04, 0x09, 0x01, 0x01, 0xFF}));
    CHECK(!pan_tilt_drive(0, 1, 1, PanDirection::Stop, TiltDirection::Stop));
    CHECK(!pan_tilt_drive(1, 0, 1, PanDirection::Stop, TiltDirection::Stop));
    CHECK(!pan_tilt_drive(1, 1, 0x15, PanDirection::Stop, TiltDirection::Stop));

    const auto zoom_fixed = zoom(1, ZoomDirection::Tele);
    const auto zoom_variable = zoom(1, ZoomDirection::Wide, 7);
    const auto zoom_stop = zoom(1, ZoomDirection::Stop);
    CHECK(bytes_equal(*zoom_fixed, {0x81, 0x01, 0x04, 0x07, 0x02, 0xFF}));
    CHECK(bytes_equal(*zoom_variable, {0x81, 0x01, 0x04, 0x07, 0x37, 0xFF}));
    CHECK(bytes_equal(*zoom_stop, {0x81, 0x01, 0x04, 0x07, 0x00, 0xFF}));
    CHECK(!zoom(1, ZoomDirection::Tele, 8));

    const auto recall = preset(2, PresetOperation::Recall, 5);
    const auto store = preset(2, PresetOperation::Store, 1);
    CHECK(bytes_equal(*recall, {0x82, 0x01, 0x04, 0x3F, 0x02, 0x04, 0xFF}));
    CHECK(bytes_equal(*store, {0x82, 0x01, 0x04, 0x3F, 0x01, 0x00, 0xFF}));
    CHECK(!preset(1, PresetOperation::Recall, 0));
    CHECK(!preset(1, PresetOperation::Recall, 51));

    CHECK(bytes_equal(*focus_mode(1, true), {0x81, 0x01, 0x04, 0x38, 0x02, 0xFF}));
    CHECK(bytes_equal(*focus_drive(1, FocusDrive::Near),
                      {0x81, 0x01, 0x04, 0x08, 0x03, 0xFF}));
    CHECK(bytes_equal(*iris(1, IrisAction::Up), {0x81, 0x01, 0x04, 0x0B, 0x02, 0xFF}));
    CHECK(bytes_equal(*white_balance(1, WhiteBalanceMode::Outdoor),
                      {0x81, 0x01, 0x04, 0x35, 0x02, 0xFF}));

    const std::uint8_t ack[]{0x90, 0x41, 0xFF};
    const std::uint8_t completion[]{0x90, 0x51, 0xFF};
    const std::uint8_t error[]{0x90, 0x61, 0x02, 0xFF};
    const std::uint8_t bad[]{0x90, 0x41, 0x00};
    CHECK(parse_response(ack, sizeof(ack)).type == ResponseType::Ack);
    CHECK(parse_response(completion, sizeof(completion)).type == ResponseType::Completion);
    CHECK(parse_response(error, sizeof(error)).error_code == 0x02);
    CHECK(!parse_response(bad, sizeof(bad)).valid);
}

void test_joystick() {
    ptz::JoystickConfig config;
    config.filter_alpha = 1.0F;
    config.pan.dead_zone = 0.10F;
    config.pan.curve = 1.0F;
    config.tilt.dead_zone = 0.10F;
    config.tilt.curve = 1.0F;
    config.zoom.dead_zone = 0.10F;
    config.zoom.curve = 1.0F;
    ptz::JoystickProcessor joystick(config);

    const auto center = joystick.update({2048, 2048, 2048}, true);
    CHECK(center.valid && center.neutral());
    const auto noise = joystick.update({2100, 2000, 2050}, true);
    CHECK(noise.neutral());
    const auto maximum = joystick.update({4095, 4095, 4095}, true);
    CHECK(std::fabs(maximum.pan - 1.0F) < 0.001F);
    CHECK(std::fabs(maximum.tilt - 1.0F) < 0.001F);
    const auto minimum = joystick.update({0, 0, 0}, true);
    CHECK(std::fabs(minimum.zoom + 1.0F) < 0.001F);
    CHECK(joystick.update({2048, 2048, 2048}, true).neutral());
    CHECK(!joystick.update({2048, 2048, 2048}, false).valid);

    config.pan.inverted = true;
    ptz::JoystickProcessor inverted(config);
    CHECK(inverted.update({4095, 2048, 2048}, true).pan < -0.99F);

    config.pan.center = 0;
    ptz::JoystickProcessor invalid(config);
    CHECK(!invalid.configuration_valid());
    CHECK(!invalid.update({0, 0, 0}, true).valid);
}

void test_discrete_inputs() {
    ptz::DebouncedButton button(20);
    CHECK(button.update(true, 0) == ptz::InputEvent::None);
    CHECK(button.update(false, 5) == ptz::InputEvent::None);
    CHECK(button.update(true, 10) == ptz::InputEvent::None);
    CHECK(button.update(true, 29) == ptz::InputEvent::None);
    CHECK(button.update(true, 30) == ptz::InputEvent::Pressed);
    CHECK(button.pressed());
    CHECK(button.update(false, 40) == ptz::InputEvent::None);
    CHECK(button.update(false, 60) == ptz::InputEvent::Released);

    ptz::QuadratureEncoder encoder;
    encoder.reset(false, false);
    CHECK(encoder.update(true, false) == 0);
    CHECK(encoder.update(true, true) == 0);
    CHECK(encoder.update(false, true) == 0);
    CHECK(encoder.update(false, false) == 1);
    CHECK(encoder.update(false, true) == 0);
    CHECK(encoder.update(true, true) == 0);
    CHECK(encoder.update(true, false) == 0);
    CHECK(encoder.update(false, false) == -1);

    encoder.reset(false, false);
    CHECK(encoder.update(true, true) == 0);  // impossible two-bit jump
}

void test_routing_and_nextion() {
    ptz::CameraRouter router;
    CHECK(router.route(1)->transport_port == 0);
    CHECK(router.route(4)->transport_port == 3);
    CHECK(router.route(4)->visca_address == 1);
    CHECK(!router.route(5));
    CHECK(!router.route(0));
    CHECK(router.set_route(5, {true, 1, 3, ptz::Capability::PanTilt}));
    CHECK(router.route(5)->visca_address == 3);
    CHECK(!router.set_route(11, {true, 0, 1, ptz::Capability::PanTilt}));

    const auto text = ptz::nextion::text_command("status.camera", "CAM 2");
    const auto number = ptz::nextion::number_command("speed", 42);
    CHECK(text && frame_starts_with(*text, "status.camera.txt=\"CAM 2\""));
    CHECK(number && frame_starts_with(*number, "speed.val=42"));
    CHECK(!ptz::nextion::text_command("bad;id", "x"));
    CHECK(!ptz::nextion::text_command("status", "bad\"value"));

    const std::uint8_t event[]{0x65, 2, 7, 1, 0xFF, 0xFF, 0xFF};
    const auto parsed = ptz::nextion::parse_touch_event(event, sizeof(event));
    CHECK(parsed.valid && parsed.page == 2 && parsed.component == 7 && parsed.pressed);
    CHECK(!ptz::nextion::parse_touch_event(event, sizeof(event) - 1U).valid);
}

void test_controller_motion_and_safety() {
    FakeTransport transport;
    ptz::ControllerConfig config;
    config.expect_responses = false;
    ptz::Controller controller(transport, {}, config);
    controller.start(0);
    CHECK(controller.state() == ptz::ControllerState::Booting);
    CHECK(controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 1) ==
          ptz::CommandResult::Disabled);
    CHECK(transport.sent.empty());
    CHECK(controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 2) ==
          ptz::CommandResult::NoChange);
    CHECK(controller.state() == ptz::ControllerState::Ready);

    CHECK(controller.apply_joystick({1.0F, -1.0F, 0.5F, true}, 10) ==
          ptz::CommandResult::Sent);
    CHECK(transport.sent.size() == 2U);
    CHECK(transport.sent[0].port == 0U);
    CHECK(bytes_equal(transport.sent[0].packet,
                      {0x81, 0x01, 0x06, 0x01, 0x09, 0x09, 0x02, 0x02, 0xFF}));
    CHECK(bytes_equal(transport.sent[1].packet, {0x81, 0x01, 0x04, 0x07, 0x22, 0xFF}));

    CHECK(controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 20) ==
          ptz::CommandResult::Sent);
    CHECK(transport.sent.size() == 4U);
    CHECK(bytes_equal(transport.sent[2].packet,
                      {0x81, 0x01, 0x06, 0x01, 0x01, 0x01, 0x03, 0x03, 0xFF}));
    CHECK(bytes_equal(transport.sent[3].packet, {0x81, 0x01, 0x04, 0x07, 0x00, 0xFF}));

    CHECK(controller.handle_button(ptz::PanelButton::SpeedFast,
                                   ptz::InputEvent::Pressed,
                                   21) == ptz::CommandResult::NoChange);
    CHECK(controller.speed_mode() == ptz::SpeedMode::Fast);
    const auto leds = controller.led_state();
    CHECK(leds[0] && leds[12]);

    CHECK(controller.handle_button(ptz::PanelButton::Camera5,
                                   ptz::InputEvent::Pressed,
                                   22) == ptz::CommandResult::Invalid);
    CHECK(controller.selected_camera() == 1);
    CHECK(controller.handle_button(ptz::PanelButton::Camera2,
                                   ptz::InputEvent::Pressed,
                                   23) == ptz::CommandResult::NoChange);
    CHECK(controller.selected_camera() == 2);

    controller.handle_button(ptz::PanelButton::Store, ptz::InputEvent::Pressed, 24);
    CHECK(controller.store_held());
    CHECK(controller.handle_button(ptz::PanelButton::Preset3,
                                   ptz::InputEvent::Pressed,
                                   25) == ptz::CommandResult::Sent);
    CHECK(transport.sent.back().port == 1U);
    CHECK(bytes_equal(transport.sent.back().packet,
                      {0x81, 0x01, 0x04, 0x3F, 0x01, 0x02, 0xFF}));
    controller.handle_button(ptz::PanelButton::Store, ptz::InputEvent::Released, 26);
    CHECK(!controller.store_held());

    CHECK(controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 30) ==
          ptz::CommandResult::Sent);
    controller.tick(280);
    CHECK(controller.state() == ptz::ControllerState::InputLost);
    CHECK(controller.diagnostics().safety_stops >= 1U);
    CHECK(controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 281) ==
          ptz::CommandResult::NoChange);
    CHECK(controller.state() == ptz::ControllerState::Ready);

    CHECK(controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 290) ==
          ptz::CommandResult::Sent);
    controller.shutdown(291);
    CHECK(controller.state() == ptz::ControllerState::ShuttingDown);
    CHECK(bytes_equal(transport.sent.back().packet,
                      {0x81, 0x01, 0x06, 0x01, 0x01, 0x01, 0x03, 0x03, 0xFF}));
}

void test_controller_errors_responses_and_lens() {
    FakeTransport failing;
    ptz::ControllerConfig no_replies;
    no_replies.expect_responses = false;
    ptz::Controller failed_controller(failing, {}, no_replies);
    failed_controller.start(0);
    failed_controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 1);
    failing.fail = true;
    CHECK(failed_controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 2) ==
          ptz::CommandResult::TransportError);
    CHECK(failed_controller.state() == ptz::ControllerState::TransportFault);

    FakeTransport replying;
    ptz::ControllerConfig reply_config;
    reply_config.input_timeout_ms = 1000;
    reply_config.response_timeout_ms = 100;
    ptz::Controller response_controller(replying, {}, reply_config);
    response_controller.start(0);
    response_controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 1);
    response_controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 2);
    CHECK(response_controller.communication_status() == ptz::CommunicationStatus::AwaitingReply);
    const std::uint8_t ack[]{0x90, 0x41, 0xFF};
    const std::uint8_t completion[]{0x90, 0x51, 0xFF};
    response_controller.on_transport_bytes(0, ack, sizeof(ack), 3);
    CHECK(response_controller.communication_status() == ptz::CommunicationStatus::Acknowledged);
    response_controller.on_transport_bytes(0, completion, sizeof(completion), 4);
    CHECK(response_controller.communication_status() == ptz::CommunicationStatus::Online);

    ptz::Controller timeout_controller(replying, {}, reply_config);
    timeout_controller.start(0);
    timeout_controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 1);
    timeout_controller.apply_joystick({1.0F, 0.0F, 0.0F, true}, 2);
    timeout_controller.tick(102);
    CHECK(timeout_controller.state() == ptz::ControllerState::TransportFault);
    CHECK(timeout_controller.communication_status() == ptz::CommunicationStatus::TimedOut);
    CHECK(timeout_controller.diagnostics().response_timeouts == 1U);

    ptz::CameraRouter lens_router;
    const auto all_capabilities = ptz::Capability::PanTilt | ptz::Capability::Zoom |
                                  ptz::Capability::Presets | ptz::Capability::Focus |
                                  ptz::Capability::Iris | ptz::Capability::WhiteBalance;
    CHECK(lens_router.set_route(1, {true, 0, 1, all_capabilities}));
    FakeTransport lens_transport;
    ptz::Controller lens_controller(lens_transport, lens_router, no_replies);
    lens_controller.start(0);
    lens_controller.apply_joystick({0.0F, 0.0F, 0.0F, true}, 1);
    CHECK(lens_controller.focus_step(1, 10) == ptz::CommandResult::Sent);
    CHECK(lens_transport.sent.size() == 2U);  // manual mode, then focus drive
    lens_controller.tick(90);
    CHECK(lens_transport.sent.size() == 3U);
    CHECK(bytes_equal(lens_transport.sent.back().packet,
                      {0x81, 0x01, 0x04, 0x08, 0x00, 0xFF}));
    CHECK(lens_controller.iris_step(-1, 91) == ptz::CommandResult::Sent);
    CHECK(lens_controller.set_white_balance(ptz::visca::WhiteBalanceMode::Auto, 92) ==
          ptz::CommandResult::Sent);
    CHECK(lens_controller.handle_button(ptz::PanelButton::AutoIris,
                                        ptz::InputEvent::Pressed,
                                        93) == ptz::CommandResult::Unsupported);
}

}  // namespace

int main() {
    test_visca_packets();
    test_joystick();
    test_discrete_inputs();
    test_routing_and_nextion();
    test_controller_motion_and_safety();
    test_controller_errors_responses_and_lens();

    if (failures == 0) {
        std::cout << "PASS: " << checks << " checks\n";
        return 0;
    }
    std::cerr << "FAIL: " << failures << " of " << checks << " checks failed\n";
    return 1;
}
