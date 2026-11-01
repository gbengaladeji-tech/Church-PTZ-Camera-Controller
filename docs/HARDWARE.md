# Hardware design status

This document distinguishes selected parts from electrically verified parts.
Nothing listed as planned or proposed should be treated as installed or safe to
connect.

## Current owner-selected baseline

| Item | Planned part | Role | Verification state |
|---|---|---|---|
| Main controller | WIZnet W55RP20-EVB-PICO | RP2040-class MCU plus W5500 Ethernet | Selected; exact received board/revision not confirmed here |
| Joystick | ServoCity 605616 | Three potentiometer axes for pan/tilt/twist zoom | Selected; terminal map, travel, center, and actual ADC range must be measured |
| Display | Nextion NX4024T032_011 | Status, settings, diagnostics | Selected/previously described as owned; exact rear-label revision and logic levels unverified |
| Switches | 28 × Omron B3F-4050 | CAM, presets, speed, autofocus, auto iris, store | Latest explicit requirement; physical stock/count not reverified |
| Caps | Omron B32-1310 | Operator button caps | Selected; panel/PCB stack and legends unverified |
| LEDs | 13 × separate red 3 mm LEDs | Operator status | Latest explicit requirement; exact MPN, current, optics, and mapping unresolved |
| Encoders | 3 × Bourns PEC11R | Focus, iris, menu | Selected family; exact suffix/detents and purchased status must be confirmed |
| Camera connectors | 4 × Amphenol RJHSE5080 | Non-magnetic 8P8C RS-422 ports | Candidate/selected connector; contact mapping and mechanical fit unverified |
| Enclosure | About 400 × 230 mm sloped panel | Physical console | Concept geometry, not manufacturing release |

## W55RP20 resource assessment

WIZnet documents the board as an RP2040 plus W5500 device with two hardware
UARTs, two PIO blocks/eight state machines, and a 12-bit ADC. On the EVB-PICO,
GPIO17 and GPIO20–25 are unavailable; GPIO16, 18, 19, and 29 have board
functions. The practical exposed control set is therefore GP0–15 and GP26–28.
GP26–28 are the natural three joystick ADC inputs. Do not allocate GP22 from a
generic Pico diagram.

Direct wiring is impossible. The raw requirement is at least:

| Function | Raw MCU signals/channels |
|---|---:|
| 28 buttons | 28 digital inputs |
| 3 encoders | 6 digital inputs |
| 13 separate LEDs | 13 digital outputs |
| Three-axis joystick | 3 ADC inputs |
| Nextion | 1 TX + 1 RX |
| Four full-duplex camera links | 4 TX + 4 RX |

This exceeds the exposed pins before power control, enables, service signals,
or spare test points are counted.

### Required expansion

- **Inputs:** 34 contact signals require at least five cascaded 8-bit parallel-
  in/serial-out registers such as a qualified 74HC165-family implementation.
  Five devices provide 40 bits. The exact family, voltage, pull resistors,
  Schmitt conditioning, connector partition, scan rate, and bit order remain to
  be designed.
- **LEDs:** 13 outputs require at least two 8-bit serial output stages. A
  74HC595 must not be assumed to drive arbitrary LED current directly; use
  properly calculated resistors and qualified sink stages or an LED-driver IC.
  Hardware output-enable and pull states must prevent startup flashes.
- **Serial:** four camera UARTs plus one display UART create five simultaneous
  serial interfaces. The MCU has only two hardware UARTs. The W55RP20 also uses
  PIO resources for its W5500 path, so a UART-plus-PIO plan needs a measured
  resource/timing proof. Alternatives include an external multi-UART device or
  a reviewed switched-transceiver bank when only one physical camera is active.
  None is released yet.

The shift chains reduce the GPIO count, but the remaining proposal still has
almost no margin. A final allocation must include UART alternate-function
limits, PIO state machines, DMA/IRQ load, BOOTSEL/RUN/SWD access, and Ethernet
operation.

## RS-422 interface

The earlier engineering review identifies TI AM26LV31E (quad driver) and
AM26LV32E (quad receiver) as candidates for four full-duplex ports. They are not
approved parts yet. Required unresolved items include:

- actual PTR-10/T MARK II 8P8C contact map and polarity;
- whether one common/reference conductor is required and how it bonds to logic
  ground/chassis;
- cable impedance, length, shield, and existing termination;
- receiver termination and guaranteed idle/failsafe bias;
- driver/receiver enable topology for startup and routing;
- ESD/transient protection appropriate to the cable environment;
- isolation decision based on measured ground difference;
- 3.3 V logic compatibility and worst-case current/thermal budget; and
- loopback/test access before any church-equipment connection.

RS-422 carries each signal as a voltage difference between a pair. It is not
Ethernet even when both use an 8P8C connector.

## Joystick electrical concept

The selected joystick is described as three passive potentiometers. The safe
proposal is to excite the tracks from the same 3.3 V/reference domain used by
the ADC, connect the wipers to GP26/27/28 through reviewed filtering/protection,
and reference them to analog ground. Never feed a bare RP2040 ADC input from a
5 V-excited potentiometer.

Before assigning directions, measure each axis at mechanical minimum, released
center, and maximum; verify which terminals are wiper/endpoints; watch for
open-circuit behavior; and record noise over time. Those measurements become
the firmware calibration, not guessed numbers.

## Display interface

The Nextion needs power plus TTL serial. Its exact `_011` hardware revision,
current consumption, TX high voltage, RX input limits, power-off injection, and
default baud rate must be checked from the label/manual and with measurements.
A one-way buffer or level shifter may be required in each direction; a generic
bidirectional level-shifter board is not automatically correct for UART.

## Buttons, encoders, and LEDs

- B3F-4050 switches are dry momentary contacts. Use pull-ups/pull-downs and
  software debounce; do not route LED current through switch contacts as though
  the caps were illuminated buttons.
- PEC11R is mechanical quadrature. Two phase signals per encoder reveal
  direction. Edge conditioning and scan timing must preserve fast turns.
- The 13 red LEDs are separate components. A proposed default is CAM 1–10 plus
  SLOW/MEDIUM/FAST, matching the current firmware's 13-state output. This
  mapping needs owner confirmation and remains configurable at the HAL/UI
  boundary.

## Power and protection gaps

The older review proposed an external regulated 5 V supply, but the exact
adapter, inlet, fusing, reverse-polarity/backfeed protection, display branch
protection, 3.3 V load, decoupling, chassis bond, and USB-plus-DC behavior are
not released. Do not power the board through VBUS and an external rail without
reviewing every current path.

## Primary sources

- [W55RP20-EVB-PICO documentation](https://docs.wiznet.io/Product/Chip/MCU/W55RP20/w55rp20-evb-pico)
- [Datavideo PTR-10 MARK II product and protocol downloads](https://datavideo.com/global/product/PTR-10%2BMark%2BII)
- [Datavideo VISCA protocol page](https://datavideo.com/us/protocol/182/ptr-10t-mark-ii-visca-control-protocol)

See [Reference Review](REFERENCE_REVIEW.md) for the local evidence and its
limitations.
