#include "ptz/router.hpp"

namespace ptz {

CameraRouter::CameraRouter() {
    constexpr Capability kDefault =
        Capability::PanTilt | Capability::Zoom | Capability::Presets;
    for (std::uint8_t camera = 1; camera <= 4; ++camera) {
        routes_[camera - 1U] = CameraRoute{true,
                                          static_cast<std::uint8_t>(camera - 1U),
                                          1U,
                                          kDefault};
    }
}

std::optional<CameraRoute> CameraRouter::route(std::uint8_t logical_camera) const {
    if (logical_camera < 1U || logical_camera > routes_.size()) {
        return std::nullopt;
    }
    const auto selected = routes_[logical_camera - 1U];
    if (!selected.enabled) {
        return std::nullopt;
    }
    return selected;
}

bool CameraRouter::set_route(std::uint8_t logical_camera, CameraRoute route_value) {
    if (logical_camera < 1U || logical_camera > routes_.size() ||
        route_value.transport_port > 9U || route_value.visca_address < 1U ||
        route_value.visca_address > 7U) {
        return false;
    }
    routes_[logical_camera - 1U] = route_value;
    return true;
}

}  // namespace ptz
