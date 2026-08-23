# Testing Plan

## Stage 1 — Software simulation

Verify that each operator action produces the intended internal command without hardware attached.

Tests:

- select Camera 1–4
- pan left/right
- tilt up/down
- stop
- zoom in/out command intent
- speed changes
- preset selection
- invalid input
- movement-disabled state

## Stage 2 — Command validation

Compare generated VISCA packet bytes against manufacturer documentation before transmitting them.

Record:

- command name
- expected packet
- generated packet
- pass/fail
- source/document section used for validation

## Stage 3 — Input hardware

Verify joystick/buttons produce stable, repeatable software input.

Measure:

- joystick center/dead zone
- minimum/maximum values
- button bounce
- disconnect behavior
- speed-control range

## Stage 4 — RS-422 bench test

Only after pinout and electrical requirements are verified:

- verify interface configuration
- verify transmit wiring
- verify no unexpected transmission on startup
- verify stop command is immediately available

## Stage 5 — Controlled PTR-10/T test

Initial sequence:

1. Select one test camera/head.
2. Enable movement.
3. Command low-speed pan left briefly.
4. Stop.
5. Command low-speed pan right briefly.
6. Stop.
7. Test tilt briefly.
8. Stop.
9. Test one supported zoom command.
10. Recall one known safe preset only after preset behavior is verified.

All unexpected behavior should be logged before continuing.

## Reliability target

Before deployment, run repeated control tests and record failures. The final system should recover safely from restarts, unplugged input hardware, invalid commands, and communication loss.
