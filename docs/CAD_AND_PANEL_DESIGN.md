# CAD and Control-Panel Design

## Design goal

Create a compact, professional, serviceable PTZ controller that is comfortable for volunteer operators and can be manufactured with a Bambu Lab A1 Mini plus selectively fabricated metal parts where they materially improve durability.

The controller should be inspired by professional PTZ workflows, but it should not be a visual or mechanical copy of the Datavideo RMC-180 MARK II.

## Current panel concept

The front surface should be divided into clear functional zones:

```text
+--------------------------------------------------------------+
| CAM 1-10 / PRESETS | STATUS + FUNCTIONS |                   |
|                    |                    |     JOYSTICK       |
| ZOOM / FOCUS       | SPEED / MENU       |   pan/tilt/twist   |
|                    | STOP / LOCK        |                   |
+--------------------------------------------------------------+
```

This is a layout concept, not a dimensioned drawing.

## Zone A — CAM 1-10 and presets

- ten clearly labelled camera-selection buttons
- strong visual indication of the active camera/profile
- CAM 1-4 correspond to the initial RS-422 profiles
- CAM 5-10 remain visibly unassigned/disabled until future network profiles exist
- preset buttons should be reachable without crossing over the joystick
- common shots should be easy to recall quickly

## Zone B — status and functions

- small display showing active CAM/profile and important state
- speed indication
- menu/value adjustment where needed
- warning/error state if a profile is unavailable
- no unnecessary telemetry clutter

## Zone C — joystick

- dominant physical control
- comfortable right-hand access for the intended operator position
- pan/tilt through X/Y movement
- twist axis preferred for zoom if the selected joystick supports it well
- enough surrounding clearance to avoid accidental button presses

## Zone D — STOP / lock

- STOP or movement-disable must be easy to identify by touch and sight
- should not be placed where normal joystick use can accidentally trigger it
- startup state should be non-moving

## Rear I/O concept

The rear panel should visually separate network and camera-control connections.

Proposed groups:

- RS-422 CAM 1
- RS-422 CAM 2
- RS-422 CAM 3
- RS-422 CAM 4
- LAN / Ethernet
- DC power
- service/programming access if required
- future tally/auxiliary connections only if implemented

The RS-422 ports should be labelled **CAM CONTROL / RS-422 — NOT ETHERNET** or equivalent.

## Enclosure architecture

Because of the Bambu Lab A1 Mini build volume, the controller should be intentionally modular.

Likely modules:

1. left CAM/preset module
2. centre display/function module
3. right joystick module
4. removable rear-I/O panel
5. removable bottom/service covers

Modules should align with screws, tabs, or locating features rather than relying on glue for primary structure.

## Construction rules

- use M3 machine screws and heat-set inserts for frequently serviced joints
- use replaceable internal wiring harnesses where practical
- include strain relief for external cables
- avoid trapping the main PCB where the enclosure must be destroyed to remove it
- leave access for firmware/programming/debugging
- provide enough internal clearance for connector bend radius
- keep high-current/power wiring organized separately from sensitive signal wiring where practical

## CAD workflow

Do not start with a beautiful shell.

1. select real components
2. capture exact dimensions
3. model simple component envelopes
4. place controls ergonomically
5. design flat test plates
6. print and physically test
7. revise spacing
8. design internal mounts
9. split enclosure into modules
10. add cosmetic surfaces last

## Evidence to save

For each CAD revision, save:

- screenshot
- revision name/date
- measured component dimensions
- reason for layout change
- printed fit-test photo
- what fit and what did not
- next revision decision

## Current unknowns that block final dimensions

- exact joystick model
- exact button/keycap family
- exact display module
- exact rotary encoder/function-control parts
- final RS-422 connector hardware
- final PCB dimensions
- final power-input hardware

Until those parts are selected, dimensions in concept sketches should be treated as placeholders.