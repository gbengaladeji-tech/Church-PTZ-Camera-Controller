# Milestone — Hybrid Embedded Architecture Selected

**Date:** 2026-09-22
**Phase:** Hardware architecture / purchasing / CAD transition
**Target completion:** 2026-11-06

## Why the architecture changed

The August architecture used an Arduino/input device feeding a standalone Linux computer. That was useful for learning and proving the command software, but it added unnecessary hardware and complexity for the final physical controller.

The current design moves the final controller to an embedded RP2040 platform with wired Ethernet while keeping the proven Python software as a reference/test harness.

## Confirmed church equipment

- Datavideo RMC-180 MARK II controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic AG-CX350 professional 4K camcorders

The exact Panasonic model had previously been listed as unknown. It is now confirmed as AG-CX350.

## Current target architecture

```text
Physical controls
      |
      v
W5500-EVB-PICO
(RP2040 + Ethernet)
      |
      +--> controller/profile state
      +--> display/user feedback
      |
      +--> 4 x full-duplex RS-422
      |        |
      |        +--> existing PTR-10/T systems
      |
      +--> wired Ethernet
               |
               +--> future verified DVIP/IP cameras
```

## CAM 1-10 design

- CAM 1-4: existing physical RS-422 camera-control channels
- CAM 5-10: future network-camera profiles
- unassigned profiles must remain safe and must not transmit arbitrary commands

The operator experience should stay consistent regardless of transport, but future buttons are not an excuse to fake compatibility: CAM 5-10 remain unassigned until compatible network camera-control support is actually implemented and verified.

## RS-422 development strategy

Although the final controller has four physical RS-422 outputs, the first hardware milestone remains one channel.

The first channel must prove:

- correct transceiver/electrical interface
- correct pinout
- safe startup behavior
- correct device/control mode
- low-speed pan/tilt
- STOP behavior
- supported zoom/preset behavior

Only after that should the circuit be duplicated across all four channels.

## Ethernet rule

The W5500 connection is the real Ethernet port. The four RS-422 camera-control connectors may use an 8P8C/RJ45-style form factor but are **not Ethernet**. The rear panel, labels, documentation, and wiring must make that distinction obvious.

## What remains proven from the software milestone

The existing Python work remains valid evidence and a reference implementation for camera addressing, pan/tilt, diagonal movement, STOP, speed modes, zoom command generation, preset save/recall, keyboard input, Xbox analog input, Arduino serial/joystick input, input validation, and automated controller tests.

What is **not** yet proven is real RS-422 transmission to a church PTR-10/T.

## Current physical-build status

Ordered:

- soldering equipment
- heat-shrink tubing
- wire cutter

Not yet complete:

- core controller-board purchase/bring-up
- final joystick
- final display
- button/control hardware
- four-channel RS-422 electronics
- final power architecture
- final PCB/protoboard implementation
- detailed enclosure CAD
- controlled church-camera test

## Fabrication support

OSH Cut has confirmed project support through a fabrication-discount arrangement. Private discount codes are intentionally not stored in the public repository.

Additional support discussions are focused on useful engineering needs such as PCB fabrication/assembly, enclosure/control-panel fabrication, PTZ technical guidance, and development/demo hardware.

## CAD direction

The controller remains a sloped desktop console inspired by professional PTZ workflows, but not a copy of the RMC-180.

Planned physical areas:

- CAM 1-10 and presets
- display/function controls
- joystick
- zoom/focus
- STOP/lock
- rear I/O

The enclosure will be modular so each section fits within the Bambu Lab A1 Mini build volume and can be replaced or revised independently.

## November 6 target

The current goal is a functional, documented controller by 2026-11-06. The schedule is an engineering target, not permission to skip staged electrical testing.

The most important next proof is:

> RP2040 controller -> verified RS-422 interface -> one approved PTR-10/T -> safe physical movement and STOP

That milestone matters more than cosmetic enclosure completion.