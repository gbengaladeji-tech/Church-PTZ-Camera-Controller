#pragma once

#include <cstdint>

#include "ptz/types.hpp"

namespace ptz {

enum class TransportError : std::uint8_t { None, Busy, Disconnected, IoError };

struct SendResult {
    bool accepted{false};
    TransportError error{TransportError::IoError};
};

class Transport {
  public:
    virtual ~Transport() = default;
    virtual SendResult send(std::uint8_t physical_port, const Packet& packet) = 0;
};

}  // namespace ptz
