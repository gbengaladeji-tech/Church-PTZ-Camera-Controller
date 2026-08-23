# V1 Requirements

## Purpose

Create a low-cost operator controller that can eventually control the church's existing Datavideo PTR-10/T MARK II robotic camera system while being easier for volunteers to understand and operate.

## Functional requirements

- Select Camera 1–4.
- Pan left/right.
- Tilt up/down.
- Stop pan/tilt movement.
- Control zoom in/out when supported by the installed camera-control chain.
- Adjust movement speed.
- Recall named presets.
- Clearly show the active camera.
- Start in a safe non-moving state.
- Provide an operator-accessible stop function.

## User requirements

- Main controls must be understandable without reading a long manual.
- Camera selection must be obvious before movement begins.
- Common church shots should use names rather than only preset numbers.
- Frequently used controls should be physical rather than hidden in menus.
- Advanced settings should not clutter normal operation.

## Engineering constraints

- Low prototype budget.
- Reuse existing development hardware where practical.
- Do not modify or open church production equipment during early development.
- Real-hardware testing must be controlled and reversible.
- RS-422 wiring and electrical levels must be verified before connection.
- The design must not assume an RJ-45 connector means Ethernet.

## Out of scope for V1

- Autonomous speaker tracking.
- AI camera directing.
- Automatic live video switching.
- Large touchscreen interface.
- Cloud services.
- Replacing the PTR-10/T motors or motor drivers.
- Recreating every feature of the RMC-180.

## Definition of done

V1 is complete when the controller can reliably select a camera, pan/tilt, stop, control supported zoom, adjust speed, recall named presets, provide clear operator feedback, and successfully operate at least one church PTR-10/T during a controlled test.
