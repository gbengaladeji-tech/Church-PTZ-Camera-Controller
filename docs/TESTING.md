# Testing Plan

## Stage 1 — Existing software/reference tests

Maintain the current Python test harness as a known reference.

Verify camera addressing, pan/tilt, diagonals, stop, zoom command intent, speed changes, preset save/recall, invalid input rejection, and controller-state behavior.

## Stage 2 — Embedded input and state tests

On the RP2040 target, verify:

- CAM 1-10 button scanning
- selected-profile state
- unassigned CAM 5-10 behavior
- joystick centre/dead zone
- minimum/maximum joystick values
- button debounce
- speed/function controls
- STOP / movement-disable behavior
- display feedback
- input disconnect/error behavior

An unassigned CAM selection must not result in camera-control traffic.

## Stage 3 — Command validation

Compare embedded-generated commands against known-good/reference packet behavior and manufacturer documentation before transmitting them.

Record command name, selected profile, expected packet/behavior, generated packet/behavior, pass/fail, and the source/document section used for validation.

## Stage 4 — Single-channel RS-422 bench test

Before church equipment is connected:

- verify the exact transceiver/interface configuration
- verify supply voltages
- verify TX/RX polarity and pinout
- verify idle/startup behavior
- verify no unintended transmission at startup
- verify STOP is immediately available
- verify the RS-422 connector cannot be confused with Ethernet in the test setup

## Stage 5 — Controlled PTR-10/T test

Only after interface and pinout verification:

1. connect one test channel to one approved PTR-10/T system
2. start with movement disabled
3. select the correct CAM/profile
4. enable movement
5. command low-speed pan left briefly
6. STOP
7. command low-speed pan right briefly
8. STOP
9. test tilt briefly
10. STOP
11. test supported zoom
12. test one known-safe preset only after preset behavior is verified

Log every unexpected behavior before continuing.

## Stage 6 — Four-channel expansion

After one channel is proven:

- duplicate the verified RS-422 circuit
- test channels independently
- verify CAM 1-4 routing
- verify selecting one camera cannot move another
- verify switching cameras leaves movement stopped until new input is given
- verify STOP behavior on every channel

## Stage 7 — Ethernet/network validation

The W5500 Ethernet hardware can be tested independently from camera-control protocol support.

Verify link detection, IP configuration, basic network communication, and reconnect behavior.

Do **not** mark DVIP/IP camera control as complete until a specific compatible camera/protocol implementation has been verified. CAM 5-10 should remain disabled/unassigned until that point.

## Stage 8 — Operator and reliability testing

Before deployment, test repeated camera selection, movement/stop cycles, restarts, cable disconnect/reconnect, invalid input, communication-loss behavior, extended powered operation, enclosure/control ergonomics, and volunteer/operator feedback.

The final system should recover to a safe non-moving state after faults or restarts.