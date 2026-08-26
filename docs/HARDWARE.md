# Hardware Plan

## Existing church hardware observed

- Datavideo RMC-180 MARK II controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic professional 4K camcorders
- Exact Panasonic camera model still needs to be confirmed

## Current hardware direction

The project has moved past software-only prototyping. The final controller is intended to be a standalone physical console with a professional control layout and a modular 3D-printed enclosure.

Target architecture:

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
Python controller software
      |
      v
verified RS-422 interface
      |
      v
Datavideo PTR-10/T
```

Planned physical features:

- large 3-axis joystick for pan / tilt / twist zoom
- four camera-selection controls initially
- preset banks
- Slow / Medium / Fast speed controls
- dedicated Stop and Lock controls
- status display
- later focus / iris / white-balance controls only after exact camera support is verified
- clean rear I/O panel
- modular 3D-printed enclosure sized around the Bambu Lab A1 Mini build volume
- serviceable assembly using machine screws and heat-set inserts

## RS-422 development rule

Start with **one verified RS-422 channel and one PTR-10/T**. Do not buy/build a four-channel output system before the first real camera-control link is proven.

RJ45-shaped camera-control connectors are not assumed to be Ethernet. The exact electrical interface, pinout, and PTR-10/T mode must be verified before connection.

## Assembly tools and BOM

The full live checklist for workshop tools, wiring supplies, controller components, budget tracking, CAD workflow, and future missing items is maintained in:

[`BUILD_AND_DOCUMENTATION_PLAN.md`](BUILD_AND_DOCUMENTATION_PLAN.md)

That document currently includes the fact that the required assembly/tooling kit still needs to be acquired, including soldering equipment, multimeter, wire tools, hookup wire, connectors, perfboard, M3 hardware, cable management, rubber feet, labels, USB cables/adapters, and microSD tooling as needed.

## Purchase rule

Do not design the final enclosure from guessed product dimensions. Finalize high-impact components first, capture the real dimensions/datasheets, then build the CAD around those exact parts.

Do not connect experimental wiring to church production equipment until the software output, RS-422 interface, pinout, mode, and test procedure have been verified and permission has been obtained.
