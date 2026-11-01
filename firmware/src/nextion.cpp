#include "ptz/nextion.hpp"

#include <array>
#include <charconv>
#include <string_view>

namespace ptz::nextion {
namespace {

bool valid_identifier(std::string_view identifier) {
    if (identifier.empty()) {
        return false;
    }
    for (std::size_t index = 0; index < identifier.size(); ++index) {
        const char value = identifier[index];
        const bool alpha = (value >= 'A' && value <= 'Z') ||
                           (value >= 'a' && value <= 'z') || value == '_';
        const bool digit = value >= '0' && value <= '9';
        if ((!alpha && !(index > 0U && (digit || value == '.'))) ||
            (index == 0U && !alpha)) {
            return false;
        }
    }
    return true;
}

bool safe_text(std::string_view value) {
    for (const char character : value) {
        if (character < 0x20 || character == '"' || character == '\\') {
            return false;
        }
    }
    return true;
}

bool append(Frame& frame, std::string_view value) {
    if (frame.size + value.size() > frame.bytes.size()) {
        return false;
    }
    for (const char character : value) {
        frame.bytes[frame.size++] = static_cast<std::uint8_t>(character);
    }
    return true;
}

bool terminate(Frame& frame) {
    if (frame.size + 3U > frame.bytes.size()) {
        return false;
    }
    frame.bytes[frame.size++] = 0xFF;
    frame.bytes[frame.size++] = 0xFF;
    frame.bytes[frame.size++] = 0xFF;
    return true;
}

}  // namespace

std::optional<Frame> text_command(std::string_view component, std::string_view value) {
    if (!valid_identifier(component) || !safe_text(value)) {
        return std::nullopt;
    }
    Frame frame;
    if (!append(frame, component) || !append(frame, ".txt=\"") || !append(frame, value) ||
        !append(frame, "\"") || !terminate(frame)) {
        return std::nullopt;
    }
    return frame;
}

std::optional<Frame> number_command(std::string_view component, std::int32_t value) {
    if (!valid_identifier(component)) {
        return std::nullopt;
    }
    std::array<char, 16> number{};
    const auto converted = std::to_chars(number.data(), number.data() + number.size(), value);
    if (converted.ec != std::errc{}) {
        return std::nullopt;
    }
    Frame frame;
    if (!append(frame, component) || !append(frame, ".val=") ||
        !append(frame,
                std::string_view(number.data(),
                                 static_cast<std::size_t>(converted.ptr - number.data()))) ||
        !terminate(frame)) {
        return std::nullopt;
    }
    return frame;
}

TouchEvent parse_touch_event(const std::uint8_t* data, std::size_t size) {
    if (data == nullptr || size != 7U || data[0] != 0x65U || data[4] != 0xFFU ||
        data[5] != 0xFFU || data[6] != 0xFFU || data[3] > 1U) {
        return {};
    }
    return TouchEvent{data[1], data[2], data[3] == 1U, true};
}

}  // namespace ptz::nextion
