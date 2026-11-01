#include "ptz/visca.hpp"

#include <initializer_list>

namespace ptz::visca {
namespace {

std::optional<Packet> make_packet(std::initializer_list<std::uint8_t> values) {
    Packet packet;
    for (const auto value : values) {
        if (!packet.push(value)) {
            return std::nullopt;
        }
    }
    return packet;
}

}  // namespace

std::optional<std::uint8_t> camera_header(std::uint8_t address) {
    if (address < 1U || address > 7U) {
        return std::nullopt;
    }
    return static_cast<std::uint8_t>(0x80U + address);
}

std::optional<Packet> pan_tilt_drive(std::uint8_t address,
                                     std::uint8_t pan_speed,
                                     std::uint8_t tilt_speed,
                                     PanDirection pan,
                                     TiltDirection tilt,
                                     Limits limits) {
    const auto header = camera_header(address);
    if (!header || pan_speed < 1U || pan_speed > limits.pan_max || tilt_speed < 1U ||
        tilt_speed > limits.tilt_max) {
        return std::nullopt;
    }
    return make_packet({*header,
                        0x01,
                        0x06,
                        0x01,
                        pan_speed,
                        tilt_speed,
                        static_cast<std::uint8_t>(pan),
                        static_cast<std::uint8_t>(tilt),
                        0xFF});
}

std::optional<Packet> zoom(std::uint8_t address,
                           ZoomDirection direction,
                           std::uint8_t speed,
                           Limits limits) {
    const auto header = camera_header(address);
    if (!header || speed > limits.zoom_max) {
        return std::nullopt;
    }

    std::uint8_t command = 0x00;
    if (direction == ZoomDirection::Tele) {
        command = speed == 0U ? 0x02U : static_cast<std::uint8_t>(0x20U | speed);
    } else if (direction == ZoomDirection::Wide) {
        command = speed == 0U ? 0x03U : static_cast<std::uint8_t>(0x30U | speed);
    }
    return make_packet({*header, 0x01, 0x04, 0x07, command, 0xFF});
}

std::optional<Packet> preset(std::uint8_t address,
                             PresetOperation operation,
                             std::uint8_t one_based_preset,
                             Limits limits) {
    const auto header = camera_header(address);
    if (!header || one_based_preset < 1U || one_based_preset > limits.preset_count) {
        return std::nullopt;
    }
    return make_packet({*header,
                        0x01,
                        0x04,
                        0x3F,
                        static_cast<std::uint8_t>(operation),
                        static_cast<std::uint8_t>(one_based_preset - 1U),
                        0xFF});
}

std::optional<Packet> focus_drive(std::uint8_t address, FocusDrive action) {
    const auto header = camera_header(address);
    if (!header) {
        return std::nullopt;
    }
    return make_packet(
        {*header, 0x01, 0x04, 0x08, static_cast<std::uint8_t>(action), 0xFF});
}

std::optional<Packet> focus_mode(std::uint8_t address, bool automatic) {
    const auto header = camera_header(address);
    if (!header) {
        return std::nullopt;
    }
    const auto mode = static_cast<std::uint8_t>(automatic ? 0x02U : 0x03U);
    return make_packet({*header, 0x01, 0x04, 0x38, mode, 0xFF});
}

std::optional<Packet> iris(std::uint8_t address, IrisAction action) {
    const auto header = camera_header(address);
    if (!header) {
        return std::nullopt;
    }
    return make_packet(
        {*header, 0x01, 0x04, 0x0B, static_cast<std::uint8_t>(action), 0xFF});
}

std::optional<Packet> white_balance(std::uint8_t address, WhiteBalanceMode mode) {
    const auto header = camera_header(address);
    if (!header) {
        return std::nullopt;
    }
    return make_packet(
        {*header, 0x01, 0x04, 0x35, static_cast<std::uint8_t>(mode), 0xFF});
}

Response parse_response(const std::uint8_t* data, std::size_t size) {
    Response result;
    if (data == nullptr || size < 3U || data[size - 1U] != 0xFFU ||
        (data[0] & 0x0FU) != 0U || (data[0] & 0xF0U) < 0x90U) {
        return result;
    }

    result.camera = static_cast<std::uint8_t>((data[0] >> 4U) - 8U);
    result.socket = static_cast<std::uint8_t>(data[1] & 0x0FU);
    const auto kind = static_cast<std::uint8_t>(data[1] & 0xF0U);
    if (kind == 0x40U && size == 3U) {
        result.type = ResponseType::Ack;
        result.valid = true;
    } else if (kind == 0x50U && size == 3U) {
        result.type = ResponseType::Completion;
        result.valid = true;
    } else if (kind == 0x60U && size == 4U) {
        result.type = ResponseType::Error;
        result.error_code = data[2];
        result.valid = true;
    }
    return result;
}

}  // namespace ptz::visca
