#include <cstdint>

#include "pico/stdlib.h"
#include "ptz/controller.hpp"

namespace {

// Commissioning builds intentionally refuse physical transmission until the
// RS-422 pinout and the five-link serial architecture have passed review.
class CommissioningTransport final : public ptz::Transport {
  public:
    ptz::SendResult send(std::uint8_t, const ptz::Packet&) override {
        return {false, ptz::TransportError::Disconnected};
    }
};

}  // namespace

int main() {
    stdio_init_all();
    CommissioningTransport transport;
    ptz::Controller controller(transport);
    controller.start(0);

    while (true) {
        // Safe commissioning image: protocol/core code is linked, but no GPIO
        // assignment or camera transmission is enabled without verified wiring.
        tight_loop_contents();
    }
}
