#include "ptz/joystick.hpp"

#include <algorithm>
#include <cmath>

namespace ptz {

bool JoystickState::neutral(float tolerance) const {
    return valid && std::fabs(pan) <= tolerance && std::fabs(tilt) <= tolerance &&
           std::fabs(zoom) <= tolerance;
}

JoystickProcessor::JoystickProcessor(JoystickConfig config) : config_(config) {}

bool JoystickProcessor::calibration_valid(const AxisCalibration& calibration) {
    return calibration.minimum < calibration.center &&
           calibration.center < calibration.maximum && calibration.dead_zone >= 0.0F &&
           calibration.dead_zone < 1.0F && calibration.curve > 0.0F;
}

bool JoystickProcessor::configuration_valid() const {
    return calibration_valid(config_.pan) && calibration_valid(config_.tilt) &&
           calibration_valid(config_.zoom) && config_.filter_alpha > 0.0F &&
           config_.filter_alpha <= 1.0F;
}

float JoystickProcessor::normalize(std::uint16_t raw,
                                   const AxisCalibration& calibration) {
    const float offset = static_cast<float>(raw) - static_cast<float>(calibration.center);
    const float span = offset >= 0.0F
                           ? static_cast<float>(calibration.maximum - calibration.center)
                           : static_cast<float>(calibration.center - calibration.minimum);
    float value = std::clamp(offset / span, -1.0F, 1.0F);
    const float magnitude = std::fabs(value);
    if (magnitude <= calibration.dead_zone) {
        return 0.0F;
    }
    const float scaled = (magnitude - calibration.dead_zone) / (1.0F - calibration.dead_zone);
    value = std::copysign(std::pow(scaled, calibration.curve), value);
    return calibration.inverted ? -value : value;
}

JoystickState JoystickProcessor::update(const std::array<std::uint16_t, 3>& raw,
                                        bool connected) {
    if (!connected || !configuration_valid()) {
        reset();
        return {};
    }

    JoystickState sample{
        normalize(raw[0], config_.pan),
        normalize(raw[1], config_.tilt),
        normalize(raw[2], config_.zoom),
        true,
    };
    if (!initialized_) {
        filtered_ = sample;
        initialized_ = true;
        return filtered_;
    }

    const auto blend = [this](float old_value, float new_value) {
        // Returning to the calibrated dead zone must stop immediately. Filtering
        // into neutral would leave an asymptotic non-zero command.
        if (new_value == 0.0F) {
            return 0.0F;
        }
        return old_value + config_.filter_alpha * (new_value - old_value);
    };
    filtered_.pan = blend(filtered_.pan, sample.pan);
    filtered_.tilt = blend(filtered_.tilt, sample.tilt);
    filtered_.zoom = blend(filtered_.zoom, sample.zoom);
    filtered_.valid = true;
    return filtered_;
}

void JoystickProcessor::reset() {
    filtered_ = {};
    initialized_ = false;
}

}  // namespace ptz
