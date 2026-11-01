#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

namespace ptz {

using Milliseconds = std::uint32_t;

struct Packet {
    static constexpr std::size_t kCapacity = 16;
    std::array<std::uint8_t, kCapacity> bytes{};
    std::size_t size{0};

    bool push(std::uint8_t value) {
        if (size >= bytes.size()) {
            return false;
        }
        bytes[size++] = value;
        return true;
    }

    bool operator==(const Packet& other) const {
        if (size != other.size) {
            return false;
        }
        for (std::size_t index = 0; index < size; ++index) {
            if (bytes[index] != other.bytes[index]) {
                return false;
            }
        }
        return true;
    }
};

enum class Capability : std::uint16_t {
    None = 0,
    PanTilt = 1U << 0U,
    Zoom = 1U << 1U,
    Presets = 1U << 2U,
    Focus = 1U << 3U,
    Iris = 1U << 4U,
    WhiteBalance = 1U << 5U,
};

constexpr Capability operator|(Capability left, Capability right) {
    return static_cast<Capability>(static_cast<std::uint16_t>(left) |
                                   static_cast<std::uint16_t>(right));
}

constexpr bool has_capability(Capability set, Capability item) {
    return (static_cast<std::uint16_t>(set) & static_cast<std::uint16_t>(item)) != 0U;
}

enum class SpeedMode : std::uint8_t { Slow = 0, Medium = 1, Fast = 2 };

struct SpeedProfile {
    std::uint8_t pan_max;
    std::uint8_t tilt_max;
    std::uint8_t zoom_max;
};

}  // namespace ptz
