# Build, Hardware, and Documentation Plan

## Purpose

This is the live build checklist for the Church PTZ Camera Controller. It records the current architecture, what has already been proven, what still needs to be purchased/built, the CAD and testing sequence, and the evidence that should be captured.

**Target completion:** 2026-11-06.

## Current phase

The core software/reference milestone is complete. The project is now in **hardware acquisition + embedded integration + CAD**.

The final hardware direction is no longer the earlier Arduino + standalone Linux-computer architecture.

Current target:

```text
Physical controls
      |
      v
W5500-EVB-PICO / RP2040
      |
      +--> input scanning + controller state
      +--> command generation
      +--> display / feedback
      |
      +--> 4 x RS-422 channels --> existing PTR-10/T systems
      |
      +--> wired Ethernet --> future verified DVIP/IP profiles
```

## Existing proven software

The Python software remains the project's protocol/reference harness:

- `software/visca.py` — VISCA command construction
- `software/controller.py` — controller state/actions
- `software/Keyboard_test.py` — keyboard simulation
- `software/Xbox_test.py` — analog test harness
- `software/serial_input.py` — Arduino serial input
- `software/transport.py` — simulation-only transport boundary
- `software/test_controller.py` — automated assertions

This proves software behavior, **not** real RS-422 communication.

## Confirmed church hardware

- Datavideo RMC-180 MARK II
- Datavideo PTR-10/T MARK II
- Panasonic AG-CX350 professional 4K camcorders

## Camera/profile design

- CAM 1-4: four physical RS-422 profiles
- CAM 5-10: future network-camera profiles
- unassigned profiles must remain safe/disabled
- RS-422 camera ports and the real Ethernet port must remain clearly separated

## Ordered workshop items

As of 2026-09-22:

| Item | Status |
|---|---|
| Soldering equipment | Ordered |
| Heat-shrink tubing | Ordered |
| Wire cutter | Ordered |

## Workshop / assembly items still to obtain or confirm

- electronics solder, if not included with the soldering equipment
- small-wire stripper
- small flush cutters if the ordered cutter is not suitable
- small screwdriver set
- digital multimeter
- 22–26 AWG stranded hookup wire
- temporary jumper leads
- prototyping/perfboard supplies as needed
- small connectors for serviceable internal wiring
- cable-management supplies
- M3 heat-set inserts
- M3 machine screws
- rubber feet
- labels/legends
- required USB/programming cables

## Main controller parts to purchase / finalize

| Category | Planned function | Current direction | Qty | Status |
|---|---|---|---:|---|
| Main controller | Embedded MCU + Ethernet | W5500-EVB-PICO / RP2040 | 1 | Not assembled |
| RS-422 interface | Existing church-camera control | Four full-duplex channels; prove one first | 4 | Final parts/BOM to verify |
| Camera-control connectors | Dedicated rear RS-422 ports | 8P8C/RJ45-style, clearly labelled NOT LAN | 4 | To finalize |
| Joystick | Pan / tilt / twist zoom | 3-axis joystick | 1 | To finalize |
| Camera buttons | CAM selection | CAM 1-10 | 10 | To finalize |
| Preset controls | Shot presets | physical preset buttons/banks | TBD | To finalize |
| Function controls | speed / stop / lock / focus / menu | physical switches/buttons | TBD | To finalize |
| Input expansion | read larger button count | shift-register/input-expansion approach | TBD | To finalize |
| Display | active CAM/status/menu | small status display | 1 | To finalize |
| Power | stable internal rails | final rail/current design after BOM freeze | 1 system | To finalize |
| Enclosure | durable control surface | modular A1 Mini printed enclosure | 1 | CAD pending |
| Fasteners | serviceable construction | M3 screws + heat-set inserts | TBD | To purchase |
| Internal wiring | removable/serviceable harnesses | connectors + labelled stranded wire | TBD | To purchase |

## PCB / prototyping strategy

### Stage A — bench prototype

- one RS-422 channel
- minimum controls needed for testing
- safe power arrangement
- easy measurement/access

### Stage B — full electrical prototype

- four RS-422 channels
- CAM 1-10 inputs
- joystick
- display
- preset/function controls
- Ethernet hardware active for normal networking tests

### Stage C — organized/final implementation

- custom PCB or structured prototyping solution
- serviceable connectors
- labelled wiring
- enclosure mounting
- strain relief

PCBWay may be useful for PCB fabrication/assembly once the design reaches a suitable stage.

## Fabrication support

- OSH Cut has confirmed project fabrication support through a 50% discount arrangement for eligible orders through the end of 2026.
- Private sponsor discount codes must never be stored in the public repository.
- Unconfirmed sponsor discussions should not be presented as confirmed support.

## CAD plan

The physical design should follow this order:

1. select the real joystick, display, buttons, connectors, and controller hardware
2. record datasheet dimensions and measure parts
3. create simple reference/component-envelope models
4. sketch the operator layout
5. create a flat control-panel mockup
6. print small fit/ergonomic test pieces
7. divide the enclosure into A1 Mini-compatible modules
8. design internal mounts and cable paths
9. design removable rear I/O and bottom/service panels
10. only then create cosmetic/final surfaces

Likely modules:

- CAM/preset section
- display/function section
- joystick section
- rear I/O panel
- bottom/service panels

See `docs/CAD_AND_PANEL_DESIGN.md` for the current physical design concept.

## Target schedule to November 6

This is an aggressive target and should never override safe electrical validation.

### Sep 22 – Oct 1

- freeze first-round BOM
- order core controller parts
- create component-envelope CAD models
- sketch/control-panel layout

### Oct 2 – Oct 10

- bring up RP2040/W5500 development environment
- build/test input scanning
- prototype one RS-422 channel
- validate electrical interface and pinout before church connection

### Oct 11 – Oct 20

- controlled one-camera test when approved
- expand proven RS-422 design toward four channels
- implement CAM 1-10 profile logic
- integrate joystick/display/buttons

### Oct 21 – Oct 28

- complete main enclosure CAD
- print fit-test sections
- revise mounting and wiring
- assemble full electrical prototype

### Oct 29 – Nov 3

- controlled multi-camera testing
- reliability testing
- operator feedback
- fix hardware/firmware/UI issues

### Nov 4 – Nov 6

- final revisions
- clean wiring/enclosure
- final documentation
- photos/video/demo
- project retrospective

## Testing gate before church equipment

Do not connect experimental hardware to a PTR-10/T until:

- command behavior is verified
- exact RS-422 electrical interface is verified
- exact connector pinout is verified
- PTR-10/T control mode is verified
- startup behavior is safe
- STOP is available
- first test is limited to one approved camera/head
- test begins at low movement speed
- permission has been obtained

## Documentation workflow

### Obsidian = engineering notebook

After meaningful work sessions, record the goal, what changed, what was learned, mistakes/failures, measurements, decisions and reasoning, unresolved questions, and the next step.

### GitHub = technical source of truth

Keep source code/firmware, automated tests, architecture docs, BOM/hardware plan, CAD source/revisions, test procedures/results, wiring/interface documentation, and milestone documents.

### Evidence to capture

- clear prototype photos
- CAD screenshots
- wiring diagram revisions
- part numbers/datasheets
- measured dimensions
- expected vs actual test results
- failures/fixes
- terminal/test output
- short video when physical behavior first works
- operator feedback
- Git commit / CAD revision

## Open decisions

- [ ] final joystick model
- [ ] final display model
- [ ] final switch/keycap family
- [ ] exact preset-button/bank layout
- [ ] exact RS-422 transceiver implementation
- [ ] final button-input expansion parts
- [ ] final power architecture
- [ ] final rear-I/O connector family
- [ ] tally implementation
- [ ] final enclosure module split/dimensions
- [ ] cooling/ventilation need
- [ ] cable strain-relief method
- [ ] exact AG-CX350 camera-specific controls supported through the installed chain
- [ ] network-camera/DVIP implementation for CAM 5-10