#pragma once

#include <cstddef>
#include <cstdint>
#include <optional>

#include "ptz/types.hpp"

namespace ptz::visca {

enum class PanDirection : std::uint8_t { Left = 0x01, Right = 0x02, Stop = 0x03 };
enum class TiltDirection : std::uint8_t { Up = 0x01, Down = 0x02, Stop = 0x03 };
enum class ZoomDirection : std::uint8_t { Stop, Tele, Wide };
enum class PresetOperation : std::uint8_t { Store = 0x01, Recall = 0x02 };
enum class FocusDrive : std::uint8_t { Stop = 0x00, Far = 0x02, Near = 0x03 };
enum class IrisAction : std::uint8_t { Reset = 0x00, Up = 0x02, Down = 0x03 };
enum class WhiteBalanceMode : std::uint8_t {
    Auto = 0x00,
    Indoor = 0x01,
    Outdoor = 0x02,
    OnePush = 0x03,
    Manual = 0x05,
};

struct Limits {
    std::uint8_t pan_max{0x18};
    std::uint8_t tilt_max{0x14};
    std::uint8_t zoom_max{0x07};
    std::uint8_t preset_count{50};
};

std::optional<std::uint8_t> camera_header(std::uint8_t address);
std::optional<Packet> pan_tilt_drive(std::uint8_t address,
                                     std::uint8_t pan_speed,
                                     std::uint8_t tilt_speed,
                                     PanDirection pan,
                                     TiltDirection tilt,
                                     Limits limits = {});
std::optional<Packet> zoom(std::uint8_t address,
                           ZoomDirection direction,
                           std::uint8_t speed = 0,
                           Limits limits = {});
std::optional<Packet> preset(std::uint8_t address,
                             PresetOperation operation,
                             std::uint8_t one_based_preset,
                             Limits limits = {});
std::optional<Packet> focus_drive(std::uint8_t address, FocusDrive action);
std::optional<Packet> focus_mode(std::uint8_t address, bool automatic);
std::optional<Packet> iris(std::uint8_t address, IrisAction action);
std::optional<Packet> white_balance(std::uint8_t address, WhiteBalanceMode mode);

enum class ResponseType : std::uint8_t { Ack, Completion, Error, Unknown };

struct Response {
    ResponseType type{ResponseType::Unknown};
    std::uint8_t camera{0};
    std::uint8_t socket{0};
    std::uint8_t error_code{0};
    bool valid{false};
};

Response parse_response(const std::uint8_t* data, std::size_t size);

}  // namespace ptz::visca
