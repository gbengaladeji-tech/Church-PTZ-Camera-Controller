#pragma once

#include <array>
#include <cstdint>

namespace ptz {

struct AxisCalibration {
    std::uint16_t minimum{0};
    std::uint16_t center{2048};
    std::uint16_t maximum{4095};
    float dead_zone{0.08F};
    float curve{1.5F};
    bool inverted{false};
};

struct JoystickConfig {
    AxisCalibration pan{};
    AxisCalibration tilt{};
    AxisCalibration zoom{};
    float filter_alpha{0.25F};
};

struct JoystickState {
    float pan{0.0F};
    float tilt{0.0F};
    float zoom{0.0F};
    bool valid{false};

    bool neutral(float tolerance = 0.001F) const;
};

class JoystickProcessor {
  public:
    explicit JoystickProcessor(JoystickConfig config = {});
    JoystickState update(const std::array<std::uint16_t, 3>& raw, bool connected);
    void reset();
    bool configuration_valid() const;

  private:
    static bool calibration_valid(const AxisCalibration& calibration);
    static float normalize(std::uint16_t raw, const AxisCalibration& calibration);

    JoystickConfig config_;
    JoystickState filtered_{};
    bool initialized_{false};
};

}  // namespace ptz
