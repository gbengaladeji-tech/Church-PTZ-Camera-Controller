#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <string_view>

namespace ptz::nextion {

struct Frame {
    static constexpr std::size_t kCapacity = 128;
    std::array<std::uint8_t, kCapacity> bytes{};
    std::size_t size{0};
};

std::optional<Frame> text_command(std::string_view component, std::string_view value);
std::optional<Frame> number_command(std::string_view component, std::int32_t value);

struct TouchEvent {
    std::uint8_t page{0};
    std::uint8_t component{0};
    bool pressed{false};
    bool valid{false};
};

TouchEvent parse_touch_event(const std::uint8_t* data, std::size_t size);

}  // namespace ptz::nextion
