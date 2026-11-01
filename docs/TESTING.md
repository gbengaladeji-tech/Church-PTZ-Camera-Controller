# Testing and verification record

Test date: 2026-11-01, America/Toronto

## Results summary

| Area | Result | Meaning |
|---|---|---|
| C++ host build | **PASS** | GCC 15.3 compiled with C++17 and warnings-as-errors |
| New firmware tests | **PASS: 114 checks** | Pure logic and fake-transport behavior passed |
| Address/undefined sanitizer run | **PASS: 114 checks** | ASan/UBSan passed with leak detection disabled |
| Existing Python `unittest` | **PASS: 4 tests** | Earlier protocol-independent command tests passed |
| Existing Python assertion suite | **PASS** | Printed `ALL CONTROLLER TESTS PASSED` |
| RP2040/W55RP20 build | **NOT BUILT** | CMake, Arm compiler, and `PICO_SDK_PATH` unavailable |
| RS-422 loopback | **NOT RUN** | Transport electronics/pinout not released |
| Nextion hardware | **NOT RUN** | Exact revision, levels, HMI project unavailable |
| PTR/camera operation | **NOT RUN** | No hardware connection was made or claimed |

## Commands run

```bash
make -C firmware test
```

Result:

```text
g++ ... -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror ...
PASS: 114 checks
```

```bash
PYTHONPATH=software python3 -m unittest discover -s software/tests -v
```

Result: four tests passed.

```bash
PYTHONPATH=software python3 software/test_controller.py
```

Result: `ALL CONTROLLER TESTS PASSED`.

An AddressSanitizer/UndefinedBehaviorSanitizer build also passed all 114 checks.
LeakSanitizer could not run under the environment's tracing/ptrace wrapper, so
`ASAN_OPTIONS=detect_leaks=0` was used for the successful ASan/UBSan run. This is
recorded as an environment limitation, not a leak test pass.

Embedded build attempt:

```bash
cmake -S firmware -B /tmp/church-ptz-pico-build \
  -DPICO_BOARD=W55RP20_EVB_PICO
```

Result:

```text
PICO_SDK_PATH is not set
cmake: command not found
```

This is a toolchain limitation, not a compile success or a source failure. The
host compiler does compile the same core sources.

## New automated coverage

The 114 checks exercise:

- pan/tilt packet bytes, distinct axis speeds, stop bytes, and invalid limits;
- fixed and variable wide/tele zoom and zoom stop;
- preset zero-based conversion and range validation;
- focus, autofocus, iris, and white-balance packet shapes;
- ACK, completion, error, and malformed reply parsing;
- joystick center, noise dead zone, extremes, curve/reversal, calibration error,
  disconnect, and immediate neutral;
- debounce timing and separate press/release;
- encoder clockwise/counter-clockwise cycles and invalid transitions;
- default four-port routing, disabled CAM 5, and custom route/address;
- Nextion text/numeric framing, terminators, identifier/text validation, and
  touch parsing;
- startup neutral interlock and displaced-start rejection;
- slow/medium/fast state and 13-LED selection state;
- camera change, rejected unmapped camera, and physical port selection;
- STORE-plus-PRESET behavior;
- pan/tilt and zoom direction changes and neutral stops;
- stale-input stop, safe recovery through neutral, and shutdown stop;
- injected transport failure and fault state;
- reply acknowledgement/completion and response timeout;
- focus manual-mode transition, timed focus stop, iris/WB gating; and
- explicit AUTO IRIS rejection.

## Verification categories

### Successfully compiled

- C++17 core and tests on the host.

### Passed automated tests

- all results listed above. A passing fake transport proves software behavior,
  not physical transmission.

### Checked against available documentation

- original prototype packet shapes and later Datavideo protocol family;
- official WIZnet board pin/peripheral availability;
- Datavideo product support for Sony VISCA/RS-422 and up to 50 pan/tilt presets;
- Nextion three-terminator command framing implemented at protocol boundary.

### Hardware testing still required

- exact ADC readings, noise, disconnection signature, and axis directions;
- button/encoder scan-chain electrical behavior and worst-case edge rate;
- LED currents, safe startup, brightness, and output driver temperature;
- Nextion supply current, logic levels, baud, HMI IDs, and touch events;
- five-link UART/PIO/external-UART timing under Ethernet and display load;
- RS-422 polarity, pinout, idle, bias, termination, common-mode range, ESD,
  ground difference, loopback, ACK/errors, unplug/reconnect;
- exact focus/iris/WB support matrix; and
- supervised one-head then four-head operation.

### Not yet implemented

- production W55RP20 HAL and physical transport;
- persistent configuration with schema/CRC;
- hardware watchdog setup and recovery proof;
- Nextion HMI assets/component contract;
- per-port multi-socket VISCA transaction queues;
- released PCB pin map and wiring harness; and
- CAM 5–10 route technology.

## Required future test order

1. Install the Pico SDK toolchain and obtain the exact W55RP20 board definition.
2. Cross-compile the commissioning image and inspect size/warnings.
3. Run USB/SWD-only boot; verify no camera TX activity.
4. Unit-test ADC and scan chains with no RS-422 hardware.
5. Run TTL UART loopback, then isolated/known-good RS-422 loopback.
6. Inject missing replies, bad bytes, stuck input, reset, and brownout.
7. Test one non-production head at minimum speed with immediate fallback.
8. Qualify features one at a time and update route capabilities.
9. Soak all four wired ports with display, encoders, and Ethernet active.
