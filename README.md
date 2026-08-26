# Church PTZ Camera Controller

**Project started:** 2026-08-23 02:55 UTC  
**Status:** Core software proven; moving into hardware integration  
**Target:** A practical PTZ camera-control system for my church media team

## About This Project

I am an aspiring engineering student with hands-on experience operating robotic camera systems for church productions. After spending time working with robotic camera controllers, I became interested in understanding how the systems work beyond simply operating them.

I decided to design and build my own PTZ camera-control system around the real needs of my church's media team. The project combines embedded electronics, software, communication protocols, control systems, CAD, user-interface design, testing, and documentation into one system intended for real use.

The goal is not to make a simple copy of an existing commercial controller. I want to study the current workflow, identify where it can be made easier for volunteers, and develop a controller that is intuitive, reliable, maintainable, and expandable.

## Existing Church System

Initial investigation identified:

- Datavideo RMC-180 MARK II camera controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic professional 4K camcorders
- RS-422 communication on the robotic-head system
- Sony VISCA-based control as a key protocol to investigate

The PTR-10/T hardware already performs the physical pan/tilt movement. This project will therefore focus on safely communicating with the existing system rather than attempting to directly replace or drive its motors.

## Version 1 Goals

V1 is intentionally limited. It is complete when the controller can reliably:

1. Select between multiple cameras.
2. Pan and tilt using a physical joystick.
3. Control zoom.
4. Adjust movement speed.
5. Recall clearly named shot presets.
6. Stop commanded movement safely.
7. Provide obvious feedback about which camera is selected.
8. Operate through a usable physical control surface.
9. Communicate successfully with at least one church PTR-10/T system.
10. Be documented well enough that another person can understand the design and testing process.

## Demo Target

The first prototype does not need to look like the final product. It should prove the control architecture:

```text
Physical controls
      |
      v
Arduino / input device
      |
      v
Computer running control software
      |
      v
VISCA command layer
      |
      v
Simulation first, then RS-422 hardware
      |
      v
Datavideo PTR-10/T MARK II
```

The simulation stage lets the software, commands, presets, input handling, and safety logic be tested before connecting anything to church production equipment.

## Current Software Milestone

The command/control architecture has now been proven through keyboard testing, Xbox analog input, Arduino serial input, and automated tests. `transport.py` is still simulation-only and currently prints VISCA packets. The next software-facing integration step is real RS-422 transport after the correct electrical interface and pinout are verified.

A full dated catch-up of the transition from the software milestone into hardware/product design is in [`docs/MILESTONE_2026-08-26.md`](docs/MILESTONE_2026-08-26.md).

## Planned Operator Controls

- Pan/tilt joystick with twist zoom
- Four camera-selection buttons
- Preset banks
- Movement-speed controls
- Movement enable/disable control
- Dedicated Stop control
- Status display
- Later camera-specific focus/exposure/white-balance controls only after support is verified

## Repository Structure

```text
.
├── README.md
├── docs/
│   ├── PROJECT_LOG.md
│   ├── MILESTONE_2026-08-26.md
│   ├── REQUIREMENTS.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── HARDWARE.md
│   ├── BUILD_AND_DOCUMENTATION_PLAN.md
│   ├── SAFETY.md
│   └── TESTING.md
├── software/
├── firmware/
├── cad/
├── images/
└── prototypes/
```

## Engineering Approach

This project is being developed in small, testable stages:

1. Document the existing system and requirements.
2. Learn the required VISCA command structure.
3. Build and test software command generation without real hardware.
4. Build a simulated transport layer.
5. Prove multiple input methods including Arduino serial input.
6. Finalize the physical BOM, tools, and modular CAD plan.
7. Add and verify an appropriate RS-422 interface.
8. Perform a controlled test with one PTR-10/T.
9. Expand to the final physical control surface and multi-camera hardware.
10. Test reliability, gather operator feedback, and document final deployment.

## Why I Am Building It

This is intended to solve a real problem rather than exist only as a demonstration. Church media systems are often operated by volunteers with different levels of experience. Clear camera selection, named shot presets, intuitive physical controls, and strong feedback can make the system easier to learn and reduce mistakes during live production.

The project also gives me a way to learn engineering through a real system with real users, existing hardware constraints, a limited budget, and a requirement for reliability.

## Project Documentation

The live hardware/tool checklist, budget table, software-layer explanation, CAD workflow, and documentation process are in [`docs/BUILD_AND_DOCUMENTATION_PLAN.md`](docs/BUILD_AND_DOCUMENTATION_PLAN.md).

The current transition milestone is documented in [`docs/MILESTONE_2026-08-26.md`](docs/MILESTONE_2026-08-26.md).

Major design decisions, failures, experiments, tests, changes, and milestones will continue to be recorded in `docs/PROJECT_LOG.md`. The goal is to preserve the engineering process, not just the final result.
