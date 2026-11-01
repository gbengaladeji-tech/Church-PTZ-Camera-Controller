#pragma once

#include <cstdint>

#include "ptz/types.hpp"

namespace ptz {

enum class InputEvent : std::uint8_t { None, Pressed, Released };

class DebouncedButton {
  public:
    explicit DebouncedButton(Milliseconds debounce_ms = 20U);
    InputEvent update(bool raw_pressed, Milliseconds now);
    bool pressed() const { return stable_pressed_; }

  private:
    Milliseconds debounce_ms_;
    Milliseconds last_change_ms_{0};
    bool raw_pressed_{false};
    bool stable_pressed_{false};
};

class QuadratureEncoder {
  public:
    explicit QuadratureEncoder(bool reversed = false);
    int update(bool channel_a, bool channel_b);
    void reset(bool channel_a = false, bool channel_b = false);

  private:
    std::uint8_t previous_{0};
    int accumulator_{0};
    bool reversed_{false};
};

enum class PanelButton : std::uint8_t {
    Camera1,
    Camera2,
    Camera3,
    Camera4,
    Camera5,
    Camera6,
    Camera7,
    Camera8,
    Camera9,
    Camera10,
    Preset1,
    Preset2,
    Preset3,
    Preset4,
    Preset5,
    Preset6,
    Preset7,
    Preset8,
    Preset9,
    Preset10,
    Preset11,
    Preset12,
    SpeedSlow,
    SpeedMedium,
    SpeedFast,
    AutoFocus,
    AutoIris,
    Store,
};

constexpr std::uint8_t kPanelButtonCount = 28U;

}  // namespace ptz
