# Build, Hardware, and Documentation Plan

## Purpose

This document is the practical build checklist for the Church PTZ Camera Controller. It records what the software already does, what hardware and workshop supplies are still needed, how the physical controller will be assembled, and how the project will be documented from this point forward.

The visual target is the polished modular controller concept developed for this project: a sloped desktop enclosure, illuminated camera/preset controls, a status display, a large pan/tilt joystick with twist zoom, and a clean rear I/O panel. The enclosure will be designed as multiple printable modules so it can be produced on a Bambu Lab A1 Mini.

## Current phase

**Core software milestone: complete and tested in simulation / input testing.**

The next engineering phase is hardware integration: finalizing the bill of materials, acquiring assembly tools, building the physical controls, adding a standalone computer, and then implementing and verifying the RS-422 transport to one PTR-10 before expanding to multiple camera ports.

## What the current software is

The software is intentionally split into layers so each part can be tested separately.

- `software/visca.py` — builds VISCA command packets for pan/tilt, zoom, camera addressing, speed modes, and presets.
- `software/controller.py` — holds controller state such as selected camera and speed mode, and exposes high-level actions such as move, zoom, save preset, and recall preset.
- `software/Keyboard_test.py` — keyboard test harness used to prove the control flow without physical hardware.
- `software/Xbox_test.py` — analog game-controller test harness used to prove joystick direction, deadzone, and speed behavior.
- `software/serial_input.py` — receives commands from the Arduino over USB serial and passes them into the controller layer.
- `software/transport.py` — output boundary. It currently prints VISCA packets for simulation. This is the file that will later transmit the packet bytes through the verified RS-422 interface.
- `software/test_controller.py` — automated assertions for controller state and expected VISCA packets.

Current proven path:

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

Final target path:

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
controller.py -> visca.py -> transport.py
      |
      v
verified RS-422 interface
      |
      v
Datavideo PTR-10/T
```

## Assembly tools and supplies I currently need

I currently do **not** have the following workshop/assembly items. Keep this as a live checklist and mark items only after they are actually acquired.

### Soldering and hand tools

- [ ] Soldering iron / temperature-controlled soldering station
- [ ] Electronics solder
- [ ] Wire strippers suitable for small electronics wire
- [ ] Small flush cutters
- [ ] Small Phillips screwdriver set
- [ ] Digital multimeter

### Wiring and electrical assembly

- [ ] Heat-shrink tubing assortment
- [ ] 22–26 AWG stranded hookup wire
- [ ] JST connector kit and matching crimp terminals/housings
- [ ] Dupont jumper leads for temporary testing
- [ ] Solderable perfboard / prototyping board
- [ ] Small zip ties and/or adhesive cable-management clips

### Mechanical assembly

- [ ] M3 heat-set inserts
- [ ] M3 machine screws in several useful lengths
- [ ] Rubber feet for the finished enclosure

### Labels, cables, and computer setup

- [ ] Electrical labels / printed legends / label material for controls and internal wiring
- [ ] Required USB cables/adapters for the standalone computer, Arduino, and RS-422 interface
- [ ] microSD reader if the development computer cannot read the standalone computer's microSD card directly

## Main controller parts still to finalize / purchase

Do not consider the exact BOM frozen until the part dimensions, electrical interfaces, Canadian price, shipping, and compatibility have been checked.

| Category | Planned function | Exact part/model | Qty | Source | Price CAD | Purchased? | CAD model/dimensions captured? |
|---|---|---|---:|---|---:|---|---|
| 3-axis joystick | Pan / tilt / twist zoom | TBD after final verification | 1 | TBD | $ | [ ] | [ ] |
| Standalone computer | Runs Python controller automatically | TBD | 1 | TBD | $ | [ ] | [ ] |
| Display | Camera/status/menu feedback | TBD | 1 | TBD | $ | [ ] | [ ] |
| Camera-select switches | CAM 1–4 | TBD | 4 | TBD | $ | [ ] | [ ] |
| Preset switches | Preset banks | TBD | TBD | TBD | $ | [ ] | [ ] |
| Function switches | Speed / stop / lock / camera functions | TBD | TBD | TBD | $ | [ ] | [ ] |
| Rotary encoders | Menu / value adjustment | TBD | TBD | TBD | $ | [ ] | [ ] |
| RS-422 interface | First real PTR-10 connection | TBD after pinout/interface verification | 1 first | TBD | $ | [ ] | [ ] |
| RJ45/8P8C camera connectors | Rear camera-control ports; NOT Ethernet | 4 final | TBD | $ | [ ] | [ ] |
| Tally connector | Rear tally input | TBD | 1 | TBD | $ | [ ] | [ ] |
| DC input + switch | Low-voltage power input / power switch | TBD | 1 each | TBD | $ | [ ] | [ ] |
| Power conversion | Safe internal low-voltage rails | TBD | TBD | TBD | $ | [ ] | [ ] |
| Enclosure filament | Prototype + final printed modules | TBD | TBD | TBD | $ | [ ] | n/a |
| Internal connectors | Serviceable removable wiring | TBD | TBD | TBD | $ | [ ] | [ ] |

### Unexpected / forgotten parts

Leave this section open. Every time assembly requires something that was not in the original plan, add it here instead of hiding the mistake.

| Date | Missing item discovered | Why it was needed | Cost | Lesson |
|---|---|---|---:|---|
| | | | $ | |
| | | | $ | |
| | | | $ | |
| | | | $ | |

## Budget tracking

Target hardware/build budget: **approximately C$200–250** if possible.

| Category | Planned | Actual |
|---|---:|---:|
| Main electronics | $ | $ |
| Controls / switches / joystick | $ | $ |
| RS-422 / rear I/O | $ | $ |
| Power | $ | $ |
| Tools and assembly supplies | $ | $ |
| 3D-printing / hardware | $ | $ |
| Shipping / tax | $ | $ |
| **Total** | **$** | **$** |

The tool purchases should be tracked separately from the controller-only cost as well, because tools such as a multimeter and soldering iron will be reusable on future engineering projects.

## Physical design plan

The controller should be designed around the **real purchased components**, not guessed dimensions from product photos.

1. Finalize and purchase the high-impact parts first, especially the joystick, switches, display, rear connectors, and standalone computer.
2. Measure each part and obtain a datasheet/drawing where possible.
3. Create simple CAD reference models or bounding boxes for every component.
4. Design the control-panel layout around hand comfort and operator workflow.
5. Print small test plates before printing a complete enclosure.
6. Split the enclosure into intentional modules that fit the A1 Mini build volume.
7. Use removable rear I/O and service panels so future electronics changes do not require reprinting the entire controller.
8. Use M3 heat-set inserts and machine screws for serviceable assembly rather than relying on glue.
9. Prototype in inexpensive filament first; only print the final cosmetic enclosure after fit and function are proven.

## Documentation workflow from now on

Documentation is part of the engineering work, not something to write at the end.

### Obsidian = engineering notebook

Use Obsidian for the human story and learning process. After every meaningful work session, record:

- what I was trying to do
- what I learned
- decisions I made and why
- mistakes / bugs / failed ideas
- how I fixed them
- measurements and observations
- questions that are still unresolved
- what I will do next

The writing can be casual and first-person. The goal is to preserve my actual thinking while it is fresh.

### GitHub = technical source of truth

Use GitHub for things another engineer should be able to inspect:

- source code
- automated tests
- firmware
- technical architecture
- BOM / hardware plan
- CAD source files and revisions
- test procedures and measured results
- wiring/interface documentation
- milestone commits

Commit after meaningful milestones rather than after every tiny edit. Commit messages should describe what changed or what was proven.

### Evidence to capture during hardware work

For each major hardware milestone, save:

- clear photos of the breadboard/prototype
- screenshots or terminal output from tests
- wiring diagram revision
- CAD screenshots and exported design revision
- exact part/model numbers
- measured dimensions that affected the design
- test result: expected vs actual
- failures and the fix
- short video when a physical feature first works
- later, operator feedback from actual church use

### Simple milestone documentation template

```text
Date:
Milestone:
Goal:

What I changed:

What I expected:

What actually happened:

Problems / bugs:

How I fixed them:

What I learned:

Evidence saved:
- photo:
- video:
- Git commit:
- CAD revision:

Next step:
```

## Before connecting church equipment

Do not connect experimental wiring to the PTR-10/T or camera system until all of the following are true:

- VISCA command bytes are verified.
- The exact RS-422 electrical interface is verified.
- The exact connector pinout is verified.
- The PTR-10/T control mode is verified.
- The first test is limited to one head/camera.
- Initial movement is tested at a low speed.
- Permission has been obtained to test on the church equipment.

RJ45-shaped camera-control connectors must never be assumed to be normal Ethernet.

## Open decisions / space for future needs

Use this section whenever a new need appears. Do not force the project to stay identical to the original plan if testing shows a better solution.

- [ ] Final exact joystick model
- [ ] Final standalone computer
- [ ] Final display
- [ ] Final switch family and keycap/legend method
- [ ] Final number of physical preset buttons / bank behavior
- [ ] Final rear I/O architecture for four camera channels
- [ ] Final tally implementation
- [ ] Final power architecture
- [ ] Final enclosure module split
- [ ] Final cooling/ventilation requirement
- [ ] Final cable strain-relief method
- [ ] Final startup/autostart configuration
- [ ] Exact Panasonic camera model and supported camera-specific controls
- [ ] Additional tools/supplies discovered during assembly
