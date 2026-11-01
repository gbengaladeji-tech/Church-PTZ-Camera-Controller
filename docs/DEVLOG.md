# Development log

## 2026-08-24 to 2026-08-26 — Original Python learning phase

Gbenga learned Python basics and serial VISCA packet structure, built camera
header/direction/speed translation, then added keyboard, Xbox, and Arduino input
simulations. Pan/tilt, zoom, speed, camera selection, and presets produced
printed packets. No physical RS-422 transport existed. The detailed original
learning record remains in `docs/PROJECT_LOG.md` and the preserved source.

## 2026-11-01 — Recovery and evidence audit

- Inspected Git before editing: `main` matched `origin/main`; the only untracked
  file was the recovered `software/controller_v1.py`.
- Created `feature/ptz-firmware-modernization` without modifying `main`.
- Compared all 38 VS Code history snapshots and their recorded timestamps.
- Proved the recovered file is byte-for-byte identical to the newest snapshot,
  `eLdw.py`; identified the larger previous snapshot as accidentally duplicated.
- Reviewed repository, handoffs, R5 review, every workbook sheet, unresolved CSV,
  and eight project-specific Obsidian notes read-only.
- Confirmed that older BOM/control counts conflict with the current owner
  instruction and documented the evidence precedence.
- Recorded the prototype's working features and communication/safety gaps.
- Commit `0362686`: `Preserve and assess recovered controller prototype`.

## 2026-11-01 — Firmware core

- Chose C++17/Pico SDK direction while preserving Python simulation value.
- Added fixed-capacity VISCA packet builders and response parsing.
- Added calibrated joystick normalization, dead zones, curves, filtering,
  inversion, and an immediate-neutral safety path.
- Added button debounce and encoder quadrature decoding.
- Added ten-position logical routing with CAM 1–4 enabled and CAM 5–10 disabled.
- Added safe startup, input timeout, route-change/shutdown stops, transport and
  reply fault handling, speed profiles, presets, focus pulse, capability gates,
  LED state, and diagnostics.
- Added testable Nextion framing without inventing display IDs.
- Added a safe commissioning entry point that cannot transmit to cameras.
- Found and fixed a timeout-status bug where the stop attempt hid the original
  communication timeout.
- Host build passed 114 checks with warnings treated as errors.
- Address/undefined sanitizer build passed the same 114 checks; leak detection
  was unavailable under the environment's ptrace wrapper.
- Existing Python suites passed four `unittest` tests plus the assertion suite.
- Pico build attempt was blocked because CMake, Arm compiler, and Pico SDK path
  were unavailable.
- Commit `f1719ab`: `Implement testable W55RP20 controller core`.
- Final safety review found that an active focus pulse also needed an immediate
  stop on input loss, route change, and shutdown; fixed and regression-tested in
  commit `3be962a`.

## 2026-11-01 — Documentation and handoff

- Rewrote the top-level project introduction and current requirements.
- Documented hardware resource limits and the five-serial-interface blocker.
- Added architecture, controls, wiring, protocol, testing, decisions, reference
  review, learning guide, and prioritized remaining work.
- Marked proposed versus verified information throughout.
- Kept personal sources and historical notes out of the repository.

## Known problems at handoff

- Production HAL and physical RS-422 transport are intentionally absent.
- The exact installed target, connector wiring, capabilities, and voltage
  interfaces are not verified.
- The five simultaneous serial links do not yet have a proven W55RP20 resource
  plan.
- No Nextion `.HMI` project/component contract was found.
- Embedded toolchain is not installed in the current environment.
- Hardware operation has not been tested or claimed.
