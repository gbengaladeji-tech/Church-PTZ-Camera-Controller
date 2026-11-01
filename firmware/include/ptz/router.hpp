#pragma once

#include <array>
#include <cstdint>
#include <optional>

#include "ptz/types.hpp"

namespace ptz {

struct CameraRoute {
    bool enabled{false};
    std::uint8_t transport_port{0};
    std::uint8_t visca_address{1};
    Capability capabilities{Capability::None};
};

class CameraRouter {
  public:
    static constexpr std::size_t kLogicalCameraCount = 10;

    CameraRouter();
    std::optional<CameraRoute> route(std::uint8_t logical_camera) const;
    bool set_route(std::uint8_t logical_camera, CameraRoute route);

  private:
    std::array<CameraRoute, kLogicalCameraCount> routes_{};
};

}  // namespace ptz
