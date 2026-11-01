# Learning guide: from a joystick to a moving camera

This guide explains the controller from first principles using the actual
project code. You do not need to know C++ before reading it.

## 1. What a microcontroller does

A microcontroller is a small computer designed to interact with electronics. It
runs one program repeatedly, reads electrical inputs, remembers state, makes
decisions, and changes outputs.

For this project, the W55RP20's RP2040 core will repeatedly do work like:

```text
read joystick and switches
-> convert readings into operator intentions
-> apply safety rules
-> build VISCA bytes
-> send through UART and RS-422
-> read camera replies
-> update screen and LEDs
-> repeat
```

Unlike a laptop program waiting for keyboard input, embedded firmware must keep
servicing many things. If it blocks while drawing the screen, it might miss an
encoder edge or fail to stop motion.

## 2. How inputs become outputs

Think of the layers as translators:

1. **Electricity:** the joystick wiper might be 1.67 V.
2. **ADC number:** the MCU converts that voltage to a number near the calibrated
   center.
3. **Normalized intent:** `JoystickProcessor` turns it into a number from -1 to
   +1.
4. **Controller state:** `Controller` decides whether movement is allowed and
   which camera/speed is selected.
5. **Protocol:** `visca::pan_tilt_drive` turns the decision into nine bytes.
6. **Physical link:** UART timing and an RS-422 driver turn bits into a
   differential electrical signal.
7. **Camera action:** the head accepts the command and reports ACK/completion or
   an error.

Separating these steps is powerful. You can test step 5 without a joystick and
step 3 without a camera.

## 3. Analog-to-digital conversion and the joystick

The joystick contains potentiometers. A potentiometer is a resistive track with
a moving wiper. If its ends connect to 3.3 V and ground, the wiper voltage moves
between those rails as the handle moves.

The ADC (analog-to-digital converter) measures voltage as a number. The RP2040
ADC is described as 12-bit, giving nominal codes 0–4095. Real readings are noisy,
and the physical center will not be exactly 2048.

`AxisCalibration` stores:

```cpp
minimum, center, maximum, dead_zone, curve, inverted
```

The code treats each side of center separately. That matters when the mechanical
travel is not perfectly symmetrical. It then clamps the result to -1…+1, makes
the center dead zone exactly zero, rescales the remaining travel, applies a
curve, and reverses the sign if required.

A curve greater than 1 makes the center gentler while preserving full output at
the edge. Noise filtering blends old and new readings, but there is one safety
exception: a raw value in the dead zone becomes zero immediately. Otherwise the
filter could slowly decay toward zero while the camera kept moving.

### Calibration exercise on a computer

Open `firmware/tests/test_main.cpp`, find `test_joystick`, and change the dead
zone from `0.10F` to `0.20F`. Run:

```bash
make -C firmware test
```

Add a reading just inside and just outside your new dead zone. This costs no
parts and shows how tests turn a requirement into evidence.

### Arduino exercise

With only an Arduino and a potentiometer/joystick from a starter kit:

1. connect pot ends to 5 V and GND **for the Arduino only**;
2. connect its wiper to `A0`;
3. print `analogRead(A0)` at about 50 Hz;
4. record minimum, released center, and maximum;
5. repeat center readings 100 times and find their spread;
6. choose a dead zone slightly larger than the normal spread.

Do not copy the Arduino's 5 V wiring onto the 3.3 V W55RP20 ADC.

## 4. Why switches bounce

Metal contacts do not change cleanly once. When they touch, they can bounce for
a few milliseconds:

```text
open, closed, open, closed, closed
```

Without debounce, one press could recall a preset several times. The
`DebouncedButton` remembers the most recent raw change and accepts it only after
it stays unchanged for the configured interval. It emits `Pressed` or
`Released`, which is why STORE can be held while another button is pressed.

### Debounce exercise

Draw a timeline for raw states at 0, 5, 10, 29, and 30 ms from
`test_discrete_inputs`. Predict the event before running the test. Then change
the debounce time and adjust the expected event.

## 5. How a rotary encoder reports direction

A PEC11R has two phase signals, A and B. They change in a Gray-code sequence so
only one bit should change at a time:

```text
00 -> 10 -> 11 -> 01 -> 00   one direction
00 -> 01 -> 11 -> 10 -> 00   the other direction
```

`QuadratureEncoder` uses the previous and current two-bit state as an index into
a transition table. Four valid quarter-steps produce one detent step. If both
bits jump at once, it discards the partial count because that transition is
ambiguous.

Button-style time debounce is dangerous here: a fast, valid phase transition
could be removed. Electrical conditioning and a sufficiently fast scan are
better tools.

## 6. State machines

A state machine gives the controller a small set of named situations and rules
for moving between them. This is clearer than many unrelated booleans.

The actual states are:

- `Booting`: not armed; waits for neutral;
- `Ready`: commands allowed;
- `InputLost`: stop attempted; neutral required to recover;
- `TransportFault`: communication failed; explicit reset required;
- `ShuttingDown`: stop attempted; no new control.

Example: a displaced joystick at startup cannot jump directly to motion because
the only safe transition from `Booting` to `Ready` requires neutral.

### State-machine exercise

Write these events on paper: power on, joystick right, joystick center, joystick
right, cable unplugged, joystick center. Walk through the states. Then compare
your result with `test_controller_motion_and_safety`.

## 7. Interrupts, timers, and a nonblocking loop

A **timer** measures when work is due. The controller uses millisecond timestamps
for debounce, input timeout, response timeout, refresh, and focus stop.

An **interrupt** briefly pauses normal code when hardware needs attention. A UART
receive interrupt might put bytes into a small ring buffer. An encoder edge or
DMA completion might also signal work. Interrupt handlers should be short: save
data, set a flag, return. Packet parsing and screen drawing belong in the main
loop.

The focus encoder demonstrates nonblocking timing. The controller sends near/far,
records `focus_stop_due_ms`, and continues other work. `tick()` later sends focus
stop. It never sleeps for 80 ms.

The final watchdog is another timer. Firmware must regularly prove it is alive.
If it stops feeding the watchdog, the MCU resets. But reset is not automatically
safe: the electrical TX/output states and remote camera motion must be considered
and tested.

## 8. UART, RS-422, and RJ45 are different ideas

UART defines the timing and framing of bits: baud rate, data bits, parity, and
stop bits. It produces one logic-level TX signal and reads one RX signal.

RS-422 changes each logic signal into a differential pair. The receiver cares
about the voltage difference between `+` and `-`, which resists noise over long
cables. Full duplex uses one pair in each direction.

An 8P8C connector is only a connector shape. Ethernet also uses 8P8C, but that
does not make the camera port Ethernet. Wiring an Ethernet switch to an unknown
RS-422 port can damage equipment.

Four ports require four transmit differential channels and four receive
channels. The proposed quad driver/receiver candidates provide that count, but
pin mapping, termination, failsafe bias, common ground, and protection are not
verified.

### Computer-only exercise

Take the packet `81 01 04 07 00 FF`. Label destination, command category,
operation, parameter, and terminator. Change only the address for camera 3, then
confirm with a new test.

## 9. How VISCA commands are formed

The original Python did this directly:

```python
packet = [camera_header, 0x01, 0x06, 0x01,
          pan_speed, tilt_speed, horizontal, vertical, 0xFF]
```

That was a good learning step. The new `visca::pan_tilt_drive` adds range checks,
an address check, named direction enums, fixed capacity, and an explicit failure
result. It prevents a malformed packet from quietly continuing as `None` and
failing somewhere unrelated.

Replies matter too. An ACK says accepted, completion says finished, and error
says something failed. A transport that only writes commands cannot provide
honest camera status.

## 10. Logical cameras and physical ports

The front panel has ten CAM positions but the hardware plan has four RS-422
ports. `CameraRouter` prevents those concepts from being mixed together.

For example, default CAM 2 means:

```text
logical camera 2 -> physical port 1 -> VISCA address 1
```

That default fits independent home-run ports but still needs real-head
verification. CAM 5 has no route, so selecting it returns an error instead of
sending to a random connector.

## 11. How the Nextion communicates

The Nextion accepts ASCII commands over UART and expects three `FF` terminators.
The code can build text and numeric assignments and parse touch event frames.

The screen artwork is separate from firmware. Each component has a page/name or
numeric ID. If those values are invented in code before the HMI exists, screen
changes will break firmware. That is why the project implements the wire format
but waits for a documented HMI contract.

### Nextion exercise without a screen

Find `test_routing_and_nextion`. Change `CAM 2` to `CAM 4`, run the test, and
inspect the expected bytes. Add a test proving that a newline in display text is
rejected.

## 12. How software controls real hardware

Software never moves metal by itself. It controls transistors and interfaces,
which create voltages and currents, which another machine interprets.

For a button LED:

```text
software bit -> shift register -> sink transistor -> LED current -> light
```

For camera movement:

```text
software bytes -> UART -> RS-422 driver -> cable -> receiver in PTR head
-> protocol parser -> motor controller -> motor current -> pan movement
```

Every arrow is a place to measure and test. If the packet test passes but the
camera does not move, start at the boundary and follow the chain rather than
randomly changing code.

## 13. Troubleshooting method

1. **Make it safe.** Disconnect production equipment and remove motion/power
   hazards.
2. **State the expected result.** Example: TX idle high; exactly nine UART bytes;
   stop within 250 ms of missing input.
3. **Test one boundary.** Raw ADC, normalized value, packet bytes, UART logic,
   RS-422 differential output, then camera reply.
4. **Change one thing.** Multiple changes destroy evidence.
5. **Record measurement and setup.** Include firmware commit, voltage, baud,
   wiring, tool, and time.
6. **Reproduce the failure.** A one-time success is not reliability.
7. **Add a regression test.** If software caused the fault, make the test fail
   before the fix and pass after it.

Useful questions:

- Is the controller `Ready`, or is it correctly refusing movement?
- Is CAM 5 rejected because it is intentionally unmapped?
- Is the packet correct for the selected route/address?
- Was it only accepted by the local transport, or acknowledged by the camera?
- Are TX+/TX− swapped? Is RX wired to RX instead of the other device's TX?
- Are logic levels safe when one device is powered off?
- Did the input scan miss edges under UART/display load?
- Did a reset flash LEDs or emit serial garbage?

## 14. Original versus improved implementation

| Original Python prototype | Improved firmware core |
|---|---|
| Keyboard loop and global state | Explicit controller state machine |
| Prints packet lists | Transport interface with injected failures |
| Four camera headers imply routing | Logical camera/port/address table |
| Fixed zoom only | Fixed and variable zoom |
| Limited validation | Address/speed/preset/range validation |
| No replies | ACK/completion/error parser and timeout |
| No input-loss handling | neutral interlock, stale-input and shutdown stop |
| No physical input processing | calibration, dead zone, debounce, encoders |
| No focus/iris safety | capability gates and timed focus stop |
| No display boundary | validated Nextion frames without fake IDs |
| A few assertions | 114 warning-clean host checks plus legacy tests |

The original is not “bad”; it is the learning foundation. The improved version
adds the structure required when software can move physical equipment.

## 15. Suggested learning sequence

1. Run all tests and deliberately break one expected byte.
2. Add a fourth user-adjustable speed profile in a temporary branch, then decide
   whether the UI actually needs it.
3. Write a small program that feeds recorded ADC samples to `JoystickProcessor`
   and prints normalized values.
4. Use Arduino serial output to capture switch bounce and encoder sequences.
5. Design the input bit-order table on paper and write tests before wiring it.
6. Build a TTL UART loopback test that never touches RS-422.
7. Build RS-422 loopback only after transceiver/power/protection review.
8. Perform the one-head supervised commissioning checklist in
   `REMAINING_WORK.md`.
