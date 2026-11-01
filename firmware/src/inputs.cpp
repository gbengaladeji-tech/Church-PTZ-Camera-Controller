#include "ptz/inputs.hpp"

#include <array>

namespace ptz {

DebouncedButton::DebouncedButton(Milliseconds debounce_ms) : debounce_ms_(debounce_ms) {}

InputEvent DebouncedButton::update(bool raw_pressed, Milliseconds now) {
    if (raw_pressed != raw_pressed_) {
        raw_pressed_ = raw_pressed;
        last_change_ms_ = now;
    }
    if (raw_pressed_ != stable_pressed_ &&
        static_cast<Milliseconds>(now - last_change_ms_) >= debounce_ms_) {
        stable_pressed_ = raw_pressed_;
        return stable_pressed_ ? InputEvent::Pressed : InputEvent::Released;
    }
    return InputEvent::None;
}

QuadratureEncoder::QuadratureEncoder(bool reversed) : reversed_(reversed) {}

int QuadratureEncoder::update(bool channel_a, bool channel_b) {
    static constexpr std::array<int, 16> kTransition{
        0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0,
    };
    const auto current = static_cast<std::uint8_t>((channel_a ? 2U : 0U) |
                                                   (channel_b ? 1U : 0U));
    const auto transition = static_cast<std::uint8_t>((previous_ << 2U) | current);
    if ((previous_ ^ current) == 3U) {
        accumulator_ = 0;
    } else {
        accumulator_ += kTransition[transition];
    }
    previous_ = current;

    if (accumulator_ >= 4) {
        accumulator_ = 0;
        return reversed_ ? -1 : 1;
    }
    if (accumulator_ <= -4) {
        accumulator_ = 0;
        return reversed_ ? 1 : -1;
    }
    return 0;
}

void QuadratureEncoder::reset(bool channel_a, bool channel_b) {
    previous_ = static_cast<std::uint8_t>((channel_a ? 2U : 0U) |
                                          (channel_b ? 1U : 0U));
    accumulator_ = 0;
}

}  // namespace ptz
