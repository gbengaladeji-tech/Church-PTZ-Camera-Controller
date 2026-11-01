# Engineering decisions

## Evidence precedence

The current user instruction dated 2026-11-01 overrides older R5/R6.7 records.
The current baseline is 28 Omron switches, 13 separate red LEDs, three PEC11R
encoders, the ServoCity 605616, the Nextion NX4024T032_011, W55RP20-EVB-PICO,
and four RS-422 ports. Older documents describing 27 illuminated APEM keys, six
encoders, a LOCK button, W5500 board, Raspberry Pi host, or other joysticks are
historical, not current requirements.

## D1 — Preserve the prototype

`software/controller_v1.py` is retained byte-for-byte as the newest VS Code
history snapshot. New work is separate so learning history is not rewritten.

## D2 — Production language: C++17/Pico SDK

Chosen for deterministic timing and direct PIO/UART/ADC/watchdog control, while
allowing the core to compile on a computer. Python remains a simulation and
learning tool. This does not claim that the production HAL is complete.

## D3 — Fixed-capacity protocol packets

The firmware uses small `std::array` buffers instead of heap-allocated packet
vectors. It validates ranges and returns `std::optional` for invalid commands.
This keeps packet construction deterministic and easy to test.

## D4 — Safe neutral before ready

Startup sends no movement and requires a valid neutral joystick. Neutral bypasses
the smoothing tail and becomes zero immediately. Input loss, route change,
shutdown, and reply timeout make a best-effort stop. Documentation explicitly
states that a local stop attempt cannot guarantee a remote device received it.

## D5 — Logical routing is not physical addressing

Ten front-panel camera positions are represented, but only four wired routes
are enabled. Each route independently specifies transport port, VISCA address,
and capabilities. CAM 5–10 reject safely. No imaginary ten-port architecture is
embedded in controller logic.

## D6 — Capability-gate uncertain features

Packet builders for focus, iris, and white balance are useful for protocol tests,
but default routes disable them. AUTO IRIS has no verified meaning and returns
unsupported. The display must communicate that honestly.

## D7 — No invented Nextion assets

The serial command layer exists, but page numbers/component IDs are not chosen
without an HMI project. Future IDs belong in one documented interface contract.

## D8 — No guessed production pin map

Expansion is definitely necessary, but exact ICs, pins, UART/PIO assignment,
RS-422 enables, and bit order await electrical proof. The commissioning image
links the core but refuses physical transmission.

## D9 — Default 13-LED interpretation is provisional

The software models CAM 1–10 and speed S/M/F indicators. This matches 13 outputs
and is useful for tests, but the physical mapping needs owner confirmation.

## D10 — Host tests require no third-party framework

The environment has GCC and `make` but no `pytest`, CMake, or Arm toolchain. A
small C++ test executable provides repeatable coverage with zero downloaded
dependencies. Existing Python `unittest` tests remain intact.

## D11 — No live hardware connection in this phase

Protocol and electrical uncertainty make transmission premature. The work stops
at a safe, tested core and documents the exact gates for one-head commissioning.
