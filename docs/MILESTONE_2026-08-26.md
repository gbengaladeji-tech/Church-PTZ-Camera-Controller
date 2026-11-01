# Milestone — Core Software Complete → Hardware Design

**Date:** 2026-08-26  
**Phase:** Software validation complete for the current V1 command path; transition into hardware/product design  
**Status:** Core controller software milestone complete. Real RS-422/PTR-10 integration is NOT complete yet.

## Why this milestone matters

The project has moved past the question of whether the controller logic can work at all. I now have a tested software path that can accept several kinds of input, maintain controller state, translate normal actions into VISCA commands, and pass the resulting packet to a transport boundary.

The next engineering problem is physical integration: choosing real controls and electronics, packaging them into a standalone controller, implementing the real RS-422 transport, and then safely testing one PTR-10.

## What is working now

### VISCA command layer

`software/visca.py` currently contains the reusable protocol-building pieces for the V1 command set that has been implemented so far:

- camera headers for Cameras 1–4
- pan/tilt direction translation
- diagonal movement
- stop
- pan/tilt speed validation
- slow / medium / fast speed values used for simulation
- basic zoom in / zoom out / zoom stop packets
- preset save and recall packet generation

Example verified pan/tilt output:

```text
83 01 06 01 04 04 03 01 FF
```

This represents Camera 3, slow speed, moving up.

Example stop output:

```text
83 01 06 01 04 04 03 03 FF
```

Example zoom-stop output:

```text
81 01 04 07 00 FF
```

### Controller/state layer

`software/controller.py` keeps the current controller state separate from the protocol details.

It currently handles:

- selected camera
- selected speed mode
- movement requests
- zoom requests
- preset save
- preset recall

The important architecture decision is that the controller layer works with normal actions such as `left`, `up_right`, `zoom_in`, or preset number `5`, while `visca.py` handles the protocol-specific bytes.

### Automated tests

`software/test_controller.py` checks important state and packet behavior with `assert` statements.

Tests include:

- valid and invalid camera selection
- valid and invalid speed selection
- movement packets
- stop packets
- zoom in / out / stop
- preset save / recall

Current test result:

```text
ALL CONTROLLER TESTS PASSED
```

This was re-run after the Git history was synchronized and the Xbox/Arduino transport milestone was rebased on top of the main software commit.

### Keyboard test harness

`software/Keyboard_test.py` is still useful as a debugging/simulation input. It proved that the controller can keep camera/speed state and generate packets repeatedly without any physical hardware.

It is NOT the intended final operator interface.

### Xbox analog test harness

`software/Xbox_test.py` was added to test analog movement behavior before building the final physical controller.

This proved:

- analog X/Y input can be turned into PTZ directions
- joystick deadzone logic is useful
- diagonals can be detected
- joystick strength can change speed mode
- zoom actions can be mapped separately
- duplicate commands can be suppressed

The Xbox controller is also only a test harness, not part of the final church controller.

### Arduino serial input

`software/serial_input.py` receives text commands from an Arduino over USB serial and passes them into the controller layer.

The communication chain was proven with messages including:

```text
CAMERA,3
SPEED,slow
MOVE,up
MOVE,stop
ZOOM,zoom_in
ZOOM,zoom_stop
```

The resulting output included:

```text
ARDUINO: CAMERA,3
Camera 3 selected
ARDUINO: SPEED,slow
Speed: slow
ARDUINO: MOVE,up
VISCA: 83 01 06 01 04 04 03 01 FF
ARDUINO: MOVE,stop
VISCA: 83 01 06 01 04 04 03 03 FF
ARDUINO: ZOOM,zoom_in
VISCA: 83 01 04 07 02 FF
ARDUINO: ZOOM,zoom_stop
VISCA: 83 01 04 07 00 FF
```

A temporary Arduino sketch was then used to send analog joystick readings. The real Arduino analog-input path was proven from physical joystick movement into Python/VISCA output.

This joystick was only a temporary prototype/test component. A final joystick has not been purchased yet.

## Current software architecture

```text
Keyboard / Xbox / Arduino input
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

`software/transport.py` is deliberately still simulation-only. It currently prints the packet instead of transmitting to church equipment.

The final intended path is:

```text
Physical controls
      |
      v
Arduino / input electronics
      |
      v
Standalone Linux computer
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
verified RS-422 interface
      |
      v
Datavideo PTR-10/T
```

## Important boundary: what is NOT done

Calling the core software milestone complete does NOT mean the finished controller is complete.

The following still need to be engineered and verified:

- real RS-422 transmission from `transport.py`
- exact RS-422 adapter/interface selection
- exact Datavideo connector pinout verification before wiring
- PTR-10 control-mode verification
- real acknowledgement/response behavior if required
- one controlled test on a real PTR-10
- final multi-camera electrical architecture
- final standalone computer and autostart setup
- final physical joystick and controls
- display/status interface
- power system
- enclosure and internal mounting
- exact Panasonic camera model before camera-specific focus/iris/gain features are considered complete

No experimental RS-422 wiring has been connected to the church camera system yet.

## Problems encountered and what they taught me

### Invalid/stale input

Earlier keyboard testing found that an invalid key could leave the previous movement stored and accidentally generate another movement packet. Rejecting the invalid input before packet generation fixed it.

Lesson: keeping controller state is useful, but old state must not be reused when a new input is invalid.

### `None` result handling

An invalid speed caused the packet builder to return `None`, and older code then tried to iterate over it.

Lesson: validation is only useful if callers also handle the rejected result safely.

### Module/file naming on Linux

Splitting the controller into modules made import behavior and Linux filename case-sensitivity matter.

Lesson: modular architecture is cleaner, but interfaces and file names must be consistent.

### Git history divergence

A software-architecture commit existed both locally and remotely with different commit hashes. After fetching, the branches showed as diverged. A safety branch was created, the new Xbox/Arduino files were committed, and the local duplicate software commit was skipped during rebase because the corresponding work already existed on remote `main`.

Final verified history included:

- `c3ad673` — Split controller logic and add automated tests
- `bb98125` — Add Xbox and Arduino input transport

Tests passed after the rebase.

Lesson: `git fetch` is useful for inspecting remote history before changing local history, and a backup branch is cheap insurance before rebasing.

### NixOS serial permissions

The Arduino was detected at `/dev/ttyACM0`, but Python initially received a permission error. The user account was added to the `dialout` group in NixOS configuration, the system was rebuilt, and after logging back in the device permissions worked.

Lesson: Linux hardware access depends on device permissions/groups, not only whether the hardware appears in `/dev`.

### Serial port already in use

Python later received `Device or resource busy` because another program had the Arduino serial port open.

Lesson: the Arduino IDE Serial Monitor and Python cannot both own the same serial port at the same time.

### Arduino IDE / Wayland GPU crash

Arduino IDE initially crashed in its GPU/Wayland process. Launching it using X11/XWayland with GPU acceleration disabled allowed it to run.

Lesson: development-tool problems are sometimes environment/graphics issues rather than problems with the embedded code.

## Product / hardware design direction now

The visual direction has been established around a polished, sloped desktop PTZ controller inspired by the workflow of the existing Datavideo controller, but the goal is not to make a literal copy.

Current design intent:

- large pan/tilt joystick
- twist zoom integrated into the joystick control
- clear Camera 1–4 selection
- preset banks
- speed controls
- dedicated stop / lock behavior
- small status/menu display
- later camera controls such as focus/iris/white-balance only after support is verified
- clean rear I/O area for camera-control connections, tally, low-voltage power, and service connections
- modular/serviceable internal construction

## A1 Mini design constraint

The final enclosure will be printed on a Bambu Lab A1 Mini, so the controller should not depend on one giant enclosure print.

The current product-design direction is to make the enclosure intentionally modular. Likely sections include:

- camera/preset section
- display/function-control section
- joystick section
- removable rear I/O panel
- removable bottom/service panels

The exact dimensions are NOT frozen yet. Final CAD should be built around real selected components and measured/datasheet dimensions instead of guessing from concept images.

## Budget / purchasing reality

Target build budget remains approximately **C$200–250 if possible**.

A major new discovery is that the project also needs a basic electronics workshop setup. The current missing-tool list includes items such as:

- soldering iron/station
- solder
- wire strippers
- flush cutters
- small screwdriver set
- multimeter
- heat-shrink tubing
- stranded hookup wire
- JST connectors
- Dupont leads
- M3 heat-set inserts and screws
- perfboard
- cable management
- rubber feet
- labels/legends
- required USB cables/adapters
- microSD reader if needed

The live purchasing/tool checklist is in `docs/BUILD_AND_DOCUMENTATION_PLAN.md`.

Reusable workshop-tool cost should be tracked separately from the cost of parts that stay in the controller.

## Documentation / evidence standard from this point

For each meaningful hardware/CAD milestone, capture:

- what the goal was
- what changed
- expected vs actual result
- failures and fixes
- measurements
- exact part numbers
- photos of physical prototypes
- screenshots of CAD or terminal output
- short videos when physical behavior first works
- Git commit / CAD revision
- what I learned
- next step

Images can live under the repository `images/` directory in organized milestone folders. Large videos should usually be hosted outside normal Git history and linked from the documentation rather than committed as large raw files.

## Authorship / assistance record

The goal is that I can explain the architecture, protocol choices, tests, failures, and design decisions myself.

Some repetitive integration/glue code and debugging assistance has been provided with AI help during the project. I have still been responsible for running the tests, observing failures, making project decisions, checking the resulting behavior, and learning the important concepts needed to explain how the system works.

This documentation should distinguish between what was actually tested/proven and what is still planned. It should not claim that real church hardware was controlled before that test actually happens.

## Next phase

Before detailed enclosure CAD:

1. Complete exact-part research and freeze the first realistic BOM.
2. Include the missing workshop tools in the financial plan.
3. Learn basic CAD skills rather than jumping directly into a complex assembly.
4. Use a sketchbook to explore operator layout and ergonomics.
5. Select and measure the actual joystick, switches, display, rear connectors, and standalone computer.
6. CAD simple component envelopes/reference models.
7. Print small ergonomic/fit test pieces before a full enclosure.
8. Separately verify the real RS-422 path and test only one PTR-10 first.

The next major milestone should be a documented **mechanical/control-layout concept + frozen first-round BOM**, followed by the first simple CAD/3D-print test piece.