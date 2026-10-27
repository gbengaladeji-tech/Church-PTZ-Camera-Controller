# V1 Requirements

## Purpose

Create a low-cost physical operator controller for the church's existing Datavideo PTR-10/T MARK II robotic camera system while building a safe path toward future network-controlled cameras.

Current target completion: **2026-11-06**.

## Functional requirements

- Provide physical CAM 1-10 selection.
- Map CAM 1-4 to four dedicated RS-422 camera-control channels.
- Reserve CAM 5-10 for future network-camera profiles.
- Keep unassigned camera profiles safely disabled.
- Pan left/right.
- Tilt up/down.
- Stop pan/tilt movement immediately.
- Control supported zoom.
- Support focus control only where verified.
- Adjust movement speed.
- Save/recall useful presets.
- Clearly show the active CAM/profile.
- Start in a safe non-moving state.
- Provide an operator-accessible STOP / movement-disable function.
- Provide one real wired Ethernet interface for future verified DVIP/IP expansion.

## User requirements

- Main controls must be understandable without reading a long manual.
- Camera selection must be obvious before movement begins.
- CAM 1-10 controls should use a consistent workflow even when the underlying transport differs.
- Common church shots should be easy to recall.
- Frequently used controls should be physical rather than hidden in menus.
- Advanced settings should not clutter normal operation.
- Disabled/unassigned camera profiles should be obvious to the operator.

## Hardware requirements

- W5500-EVB-PICO / RP2040 as the current embedded-controller direction.
- Four dedicated full-duplex RS-422 outputs for the existing camera-control system.
- One wired Ethernet interface for future network control.
- Large pan/tilt joystick with a practical zoom-control method.
- Status display.
- Ten camera-selection buttons.
- Preset and function controls.
- Serviceable modular enclosure.

## Engineering constraints

- Keep the prototype within the available project budget.
- Reuse existing development hardware where practical.
- Do not modify or open installed church production equipment during early development.
- Real-hardware testing must be controlled and reversible.
- RS-422 wiring and electrical levels must be verified before connection.
- An 8P8C/RJ45-shaped camera-control connector must never be assumed to be Ethernet.
- The real Ethernet port and the RS-422 camera ports must remain clearly separated.
- Final enclosure dimensions must be based on measured real parts.
- Enclosure modules must fit the Bambu Lab A1 Mini build volume.

## Out of scope for V1

- autonomous speaker tracking
- AI camera directing
- automatic live video switching
- cloud services
- replacing PTR-10/T motors or motor drivers
- recreating every feature of the RMC-180
- claiming DVIP/IP compatibility before a specific protocol/device path is verified

## Definition of done

V1 is complete when:

1. the physical control surface is assembled and usable;
2. CAM 1-10 selection works safely at the UI/profile level;
3. CAM 1-4 can address the intended four RS-422 channels;
4. at least one PTR-10/T has been successfully controlled during a documented real-hardware test before multi-camera deployment;
5. pan/tilt/stop and supported zoom behavior are reliable;
6. presets and active-camera feedback work as intended;
7. the controller starts and fails safely;
8. the enclosure and wiring are serviceable and labelled;
9. CAM 5-10 remain safely unassigned unless compatible network control has actually been implemented and verified;
10. the build, tests, failures, revisions, and operator feedback are documented.