# Hardware Plan

## Existing church hardware observed

Confirmed equipment:

- Datavideo RMC-180 MARK II controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic AG-CX350 professional 4K camcorders
- dedicated camera-control cabling associated with the PTR-10/T system

## Current hardware direction

The final controller is now planned as a **standalone embedded hybrid controller** rather than the earlier Arduino + Linux-computer architecture.

Primary controller platform:

- W5500-EVB-PICO
- RP2040 microcontroller
- wired W5500 Ethernet interface

Target architecture:

```text
Physical controls
      |
      v
W5500-EVB-PICO / RP2040
      |
      +----> CAM/profile logic
      |
      +----> four dedicated full-duplex RS-422 channels
      |          |
      |          +----> existing Datavideo PTR-10/T MARK II systems
      |
      +----> one wired Ethernet connection
                 |
                 +----> future verified DVIP/IP camera-control support
```

## Camera-selection architecture

The physical panel will expose **CAM 1-10**.

Planned mapping:

- CAM 1 -> RS-422 channel 1
- CAM 2 -> RS-422 channel 2
- CAM 3 -> RS-422 channel 3
- CAM 4 -> RS-422 channel 4
- CAM 5-10 -> future network-camera profiles

CAM 5-10 must not transmit arbitrary traffic when no compatible profile is configured. An unassigned camera button should select an explicitly disabled/unassigned state or provide clear feedback without sending control commands.

## RS-422 ports versus Ethernet

- The four camera-control outputs are dedicated RS-422 links.
- Their 8P8C/RJ45-style connectors must never be treated as normal Ethernet.
- The W5500 Ethernet connection is the actual network port.
- Physical labelling and rear-panel layout should make the difference obvious.

## Planned physical controls

- large 3-axis joystick for pan / tilt / twist zoom
- 10 camera-selection buttons
- preset controls / preset banks
- zoom and focus controls
- speed controls
- dedicated STOP / movement-disable control
- lock / function controls
- status/menu display
- rotary encoders where useful for values or menus

Camera-specific controls such as focus, iris, exposure, gain, and white balance should only be implemented after support through the installed control chain is verified.

## Input expansion

The design may use cascaded digital input-expansion logic / shift registers for the larger button count so the RP2040 does not dedicate one GPIO to every switch. Exact devices and PCB routing remain subject to final BOM verification.

## RS-422 development rule

Even though the final design contains four physical RS-422 outputs, development should begin with **one channel and one PTR-10/T**.

Sequence:

1. verify protocol bytes
2. verify the exact electrical interface
3. verify connector pinout
4. verify PTR-10/T control mode
5. bench-test one channel
6. perform one controlled low-speed real-camera test
7. only then duplicate the proven circuit for the other three channels

## Current purchased / ordered build supplies

As of 2026-09-22:

- soldering equipment — ordered
- heat-shrink tubing — ordered
- wire cutter — ordered

The following main controller items are not yet considered assembled/complete:

- W5500-EVB-PICO controller board
- final 3-axis joystick
- final display
- CAM 1-10 switches/keycaps
- preset/function controls
- four-channel RS-422 interface electronics
- rear I/O connectors
- power system
- final PCB/protoboard implementation
- enclosure hardware and final printed parts

## Enclosure direction

The enclosure will be designed around measured real components and printed on a Bambu Lab A1 Mini.

Likely modular sections:

- camera/preset section
- display/function section
- joystick section
- removable rear I/O panel
- removable bottom/service panels

Use serviceable assembly where possible: M3 machine screws, heat-set inserts, removable internal connectors, strain relief, labelled wiring, and replaceable external cables.

## Target

The current working target is a functional, documented controller by **2026-11-06**.

That date is a project target, not a reason to bypass electrical verification or safe staged testing.