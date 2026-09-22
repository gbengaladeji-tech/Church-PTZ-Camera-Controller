# Sponsor Project Brief

## Project

**Church PTZ Camera Controller**

Student-led engineering project by a Grade 12 student in Brampton, Ontario.

## Problem

My church uses robotic/PTZ cameras during live services and productions. The existing system works, but I want to understand the complete control path and build a physical controller that is easier for volunteers to learn, maintain, and expand.

This is intended for real use, not only as a classroom demonstration.

## Existing equipment

- Datavideo RMC-180 MARK II controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic AG-CX350 professional 4K camcorders

## Current controller architecture

The current design uses a W5500-EVB-PICO / RP2040 platform with:

- physical joystick and button controls
- CAM 1-10 operator selection
- four dedicated RS-422 camera-control outputs for the existing church system
- one wired Ethernet interface for future verified DVIP/IP camera-control support
- preset, speed, zoom/focus, STOP/lock, and status-display functions
- a modular serviceable enclosure designed around Bambu Lab A1 Mini manufacturing limits

## What has already been proven

- VISCA command generation for camera addressing, pan/tilt, stop, zoom, speed modes, and presets
- keyboard simulation
- Xbox analog control testing
- Arduino serial input
- physical analog joystick input through Arduino
- input validation and controller-state handling
- automated controller tests

## What is not yet claimed

Real RS-422 control of a church PTR-10/T has not yet been completed. The electrical interface, exact pinout/control mode, and first controlled hardware test remain part of the next engineering stage.

This distinction is deliberate: the project documentation separates simulated/proven software behavior from real-hardware validation.

## Current build phase

The project is now moving from software validation into hardware integration, PCB/prototyping, CAD, enclosure development, and controlled real-equipment testing.

Current target completion: **November 6, 2026**.

## Useful forms of support

Depending on the organization, useful support could include:

- PCB fabrication or assembly
- DFM review
- enclosure/control-panel fabrication
- technical PTZ/VISCA/RS-422 guidance
- temporary/demo development hardware
- educational/project pricing
- connectors, switches, controls, or other relevant hardware

The project does not need every company to provide hardware. Accurate engineering advice or a referral to the right technical contact can also be valuable.

## Documentation

The public repository records architecture decisions, tests, failures, safety rules, milestones, and future CAD revisions so that support can be connected to a real and documented engineering process.

Any sponsor contribution will be described accurately. Unconfirmed discussions are not presented as sponsorship.

## Safety

The project uses staged testing. One RS-422 channel will be electrically verified and tested with one approved church camera/head before expanding to the full four-channel system.

The four camera-control ports are dedicated RS-422 connections and are kept clearly separate from the real Ethernet/LAN interface.