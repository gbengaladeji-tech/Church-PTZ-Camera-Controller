# Church PTZ Camera Controller

**Project started:** 2026-08-23
**Current phase:** Hybrid embedded-hardware architecture selected; hardware acquisition, CAD, and real-interface validation underway
**Target completion:** 2026-11-06
**Goal:** Build a practical physical PTZ camera controller for real use by my church media team

## About This Project

I am a Grade 12 student in Brampton, Ontario with hands-on experience operating robotic camera systems for church productions. I am designing a PTZ controller around the real workflow of my church media team rather than building a classroom-only demo.

The project combines embedded electronics, camera-control protocols, firmware/software, PCB/interface design, CAD, user-interface design, testing, documentation, and operator feedback.

The goal is not to copy the existing controller. The goal is to learn how the system works, preserve compatibility with the church's existing equipment, and create a controller that is intuitive, reliable, maintainable, and expandable.

## Existing Church System

Confirmed equipment:

- Datavideo RMC-180 MARK II camera controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic AG-CX350 professional 4K camcorders
- dedicated RS-422 camera-control wiring on the existing robotic-head system
- Sony VISCA-style command generation already explored in software

The PTR-10/T hardware already performs the physical movement. This project focuses on safely communicating with the existing system rather than driving the motors directly.

## Current Hardware Architecture

The August PC-based architecture was useful for proving the software, but it is no longer the final hardware plan.

The current design is a standalone embedded hybrid controller:

```text
Physical controls
  |
  +-- 3-axis joystick
  +-- CAM 1-10 buttons
  +-- presets
  +-- zoom / focus controls
  +-- speed / function controls
  +-- STOP / lock
  +-- status display
  |
  v
W5500-EVB-PICO
(RP2040 + wired Ethernet)
  |
  +--> 4 x dedicated full-duplex RS-422 camera-control channels
  |      |
  |      +--> existing Datavideo PTR-10/T MARK II systems
  |
  +--> 1 x wired Ethernet connection
         |
         +--> future verified DVIP/IP camera-control support
```

### Camera-selection model

- The physical user interface has **CAM 1-10** selection buttons.
- **CAM 1-4** are intended to map to the four physical RS-422 camera-control channels.
- **CAM 5-10** are reserved as logical profiles for future network-controlled cameras.
- CAM 5-10 must remain safely unassigned until compatible network-camera support is implemented and verified.
- The Ethernet port is a real network connection and is electrically/logically separate from the dedicated RS-422 camera-control ports.

## What Has Already Been Proven

The earlier Python software remains an important test/reference harness.

Proven so far:

- VISCA packet generation for camera addressing, pan/tilt, stop, zoom, speed modes, and presets
- keyboard simulation
- Xbox analog input
- Arduino serial input
- physical analog joystick input through Arduino into the software path
- dead-zone and direction logic
- controller-state handling
- automated tests for important controller and packet behavior

Current simulated path:

```text
Keyboard / Xbox / Arduino
          |
          v
    controller.py
          |
          v
       visca.py
          |
          v
    transport.py
          |
          v
 printed VISCA packet
```

**Important:** real RS-422 transmission to a church PTR-10/T has not yet been completed. The electrical interface, connector pinout, device mode, and first controlled hardware test still need to be verified.

## Current Build Status

As of 2026-09-22:

- hybrid embedded architecture selected
- Panasonic camera identified as AG-CX350
- core software test harness completed
- soldering equipment ordered
- heat-shrink tubing ordered
- wire cutter ordered
- main controller electronics, final joystick, display, switches, and RS-422 hardware not yet assembled
- detailed enclosure CAD still to be developed around the final purchased parts
- real church-camera control test still pending

The current dated architecture milestone is documented in [docs/MILESTONE_2026-09-22.md](docs/MILESTONE_2026-09-22.md).

## Version 1 Goals

V1 should:

1. Provide CAM 1-10 physical selection with safe profile handling.
2. Control the existing church cameras through four dedicated RS-422 outputs.
3. Pan and tilt with a physical joystick.
4. Control supported zoom and focus functions.
5. Adjust movement speed.
6. Save/recall useful shot presets.
7. Provide a dedicated STOP / movement-disable function.
8. Clearly indicate the active camera/profile.
9. Include one wired Ethernet port for future verified DVIP/IP expansion.
10. Successfully complete a controlled real test with at least one PTR-10/T before multi-camera deployment.
11. Be packaged in a durable, serviceable physical enclosure.
12. Be documented well enough that another person can understand the design, testing, limitations, and revisions.

## Physical Design Direction

The current enclosure direction is a polished sloped desktop controller with:

- large 3-axis pan/tilt/twist joystick
- CAM 1-10 selection section
- preset controls
- zoom/focus controls
- status/menu display
- speed/function controls
- dedicated STOP / lock control
- rear I/O panel
- modular/serviceable construction

Because the enclosure will be printed on a Bambu Lab A1 Mini, it will be split into intentional modules rather than one oversized print.

Likely modules include:

- camera/preset section
- display/function-control section
- joystick section
- removable rear I/O panel
- removable bottom/service panels

## Development Strategy

1. Keep the existing Python software as a reference/test harness.
2. Freeze the first hardware BOM and exact component dimensions.
3. Build the embedded input/control hardware around the RP2040/W5500 platform.
4. Validate one RS-422 channel electrically before using church equipment.
5. Perform one controlled low-speed PTR-10/T test.
6. Expand the proven electrical design to four RS-422 channels.
7. Implement the CAM 1-10 profile layer.
8. Keep CAM 5-10 disabled until future network-camera support is verified.
9. Complete enclosure CAD around measured real parts.
10. Assemble, test, collect operator feedback, revise, and document the final controller.

## Engineering Standard

The project documentation distinguishes between what has actually been tested, what is planned, what is assumed, and what still needs verification.

Major design decisions, failures, measurements, tests, CAD revisions, wiring changes, and operator feedback will continue to be recorded so the engineering process is preserved, not just the final result.
## Key Project Documents

- [Current September architecture milestone](docs/MILESTONE_2026-09-22.md)
- [System architecture](docs/SYSTEM_ARCHITECTURE.md)
- [Hardware plan](docs/HARDWARE.md)
- [Build and documentation plan](docs/BUILD_AND_DOCUMENTATION_PLAN.md)
- [CAD and control-panel design](docs/CAD_AND_PANEL_DESIGN.md)
- [Testing plan](docs/TESTING.md)
- [Safety rules](docs/SAFETY.md)
- [Sponsor project brief](docs/SPONSOR_PROJECT_BRIEF.md)
- [Sponsorship and project support](docs/SPONSORSHIP_AND_SUPPORT.md)

## Confirmed Project Support

- **OSH Cut** — confirmed fabrication support for eligible project parts. Private sponsor codes and account-specific terms are intentionally not stored in the public repository.
