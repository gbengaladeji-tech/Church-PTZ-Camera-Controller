# Church PTZ Camera Controller

**Project started:** 2026-08-23 02:55 UTC  
**Status:** Planning and software prototyping  
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

The simulation stage will let the software, commands, presets, input handling, and safety logic be tested before connecting anything to church production equipment.

## Planned Operator Controls

- Pan/tilt joystick
- Zoom control
- Four camera-selection buttons
- Named preset buttons such as Pulpit, Altar, Choir, and Wide
- Movement-speed control
- Movement enable/disable control
- Stop control
- Status display in later versions

## Repository Structure

```text
.
├── README.md
├── docs/
│   ├── PROJECT_LOG.md
│   ├── REQUIREMENTS.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── HARDWARE.md
│   ├── SAFETY.md
│   └── TESTING.md
├── software/
│   ├── main.py
│   └── ptz/
│       ├── __init__.py
│       ├── commands.py
│       └── transport.py
├── firmware/
├── cad/
├── images/
└── prototypes/
```

## Engineering Approach

This project will be developed in small, testable stages:

1. Document the existing system and requirements.
2. Learn the required VISCA command structure.
3. Build and test software command generation without real hardware.
4. Build a simulated transport layer.
5. Add physical input controls.
6. Add an appropriate RS-422 interface.
7. Perform a controlled test with one PTR-10/T.
8. Add presets and multi-camera logic.
9. Design the final operator interface and enclosure.
10. Test reliability and document the final deployment.

## Why I Am Building It

This is intended to solve a real problem rather than exist only as a demonstration. Church media systems are often operated by volunteers with different levels of experience. Clear camera selection, named shot presets, intuitive physical controls, and strong feedback can make the system easier to learn and reduce mistakes during live production.

The project also gives me a way to learn engineering through a real system with real users, existing hardware constraints, a limited budget, and a requirement for reliability.

## Project Documentation

Major design decisions, failures, experiments, tests, changes, and milestones will be recorded in `docs/PROJECT_LOG.md`. The goal is to preserve the engineering process, not just the final result.
