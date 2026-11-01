# Draft pull request: Modernize the PTZ controller firmware and documentation

## Summary

This branch preserves and assesses the recovered Python prototype, adds a
host-tested C++17 firmware core for the planned W55RP20-EVB-PICO, documents the
current 28-button/three-encoder/13-separate-LED hardware baseline, and provides
a safe path toward one-camera RS-422 commissioning.

It also merges the current remote `main`, preserving the newer milestone, CAD,
build-plan, and public sponsorship documentation.

## Original project condition

- The untracked recovered `software/controller_v1.py` was the newest clean VS
  Code-history revision and only printed VISCA packets.
- Existing Python code demonstrated camera selection, pan/tilt, zoom, speeds,
  presets, Xbox input, and Arduino input.
- There was no physical RS-422 transport, response handling, input-loss
  watchdog, Nextion implementation, W55RP20 firmware, or current hardware HAL.
- Older repository/R5/R6 records conflicted with the latest explicit hardware
  decisions.

## Improvements

- Preserved the recovered prototype byte-for-byte and documented all 38 history
  snapshots, implemented features, reusable ideas, and correctness gaps.
- Added joystick calibration, dead zones, curves, reversal, filtering, and
  immediate neutral behavior.
- Added button debounce, press/release events, encoder direction, and panel
  control definitions.
- Added a ten-position route table with four wired defaults and six disabled
  positions.
- Added validated VISCA movement, variable zoom, presets, focus, iris, white
  balance, and ACK/completion/error parsing.
- Added safe startup, input timeout, shutdown/route/focus stops, response timeout,
  transport faults, recovery states, diagnostics, and 13-LED state.
- Added a testable Nextion protocol layer without inventing screen assets/IDs.
- Added a safe Pico commissioning target that cannot transmit until wiring and
  serial resources are released.
- Added GitHub Actions host/Python tests.

## Architecture change

Production firmware now targets C++17 with the Raspberry Pi Pico SDK so it can
use RP2040 PIO/UART/ADC/timers directly. Protocol and safety logic remain
host-compilable. Python stays as a preserved learning and simulation tool.

Logical camera selection is separate from physical port, VISCA address, and
capabilities. This avoids pretending the ten front-panel positions are ten
physical RS-422 ports.

## Verification performed

- C++ host build with GCC 15.3, C++17, and warnings as errors: pass.
- Firmware core/fake transport: 114 checks passed.
- AddressSanitizer/UndefinedBehaviorSanitizer: 114 checks passed with leak
  detection disabled because LeakSanitizer cannot run under the environment's
  ptrace wrapper.
- Existing Python `unittest`: four tests passed.
- Existing Python assertion suite: passed.
- Local Markdown links: passed.
- Common credential-pattern scan: passed.
- Embedded build: attempted but not run because CMake, Arm compiler, and
  `PICO_SDK_PATH` are unavailable.

## Hardware assumptions and boundaries

- No physical camera operation is claimed.
- Exact installed PTR/camera revisions, baud/mode, connector pinout, polarity,
  termination, bias, protection, and supported lens functions are unverified.
- Direct GPIO is insufficient; input shift registers and LED drivers are
  required.
- Four camera links plus Nextion create five serial interfaces; the exact
  UART/PIO/external-UART or switched-port design must be proven.
- CAM 5–10 remain disabled.
- Focus/iris/white balance remain capability-gated.
- The 13-LED CAM1–10 plus speed mapping is proposed and needs owner confirmation.

## Outstanding work

1. Verify exact hardware and Datavideo documentation/pinout.
2. Resolve serial resources, transceivers, power, protection, and Nextion levels.
3. Install the Pico SDK toolchain and implement/test the production HAL.
4. Complete disconnected TTL and RS-422 loopback tests.
5. Commission one authorized non-production head at minimum speed.
6. Qualify capabilities, then expand to four ports and reliability testing.
7. Freeze PCB/harness/enclosure only after electrical and mechanical proof.

Detailed gates are in `docs/REMAINING_WORK.md` and results in
`docs/TESTING.md`.
