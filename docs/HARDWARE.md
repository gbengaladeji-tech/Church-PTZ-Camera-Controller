# Hardware Plan

## Existing church hardware observed

- Datavideo RMC-180 MARK II controller
- Datavideo PTR-10/T MARK II robotic pan/tilt heads
- Panasonic professional 4K camcorders

## Prototype hardware

The first prototype should stay inexpensive and reuse available equipment where possible.

Planned items:

- Development computer
- Arduino Uno or similar input microcontroller
- 2-axis joystick
- Camera-selection buttons
- Preset buttons
- Zoom rocker or two buttons
- Rotary encoder/knob for speed
- LEDs or illuminated buttons for status
- Breadboard / terminal blocks / wiring
- Appropriate RS-422 interface only after software simulation works

## Final-controller hardware ideas

Possible later additions:

- Better industrial-feeling joystick
- Illuminated camera-selection buttons
- Dedicated zoom rocker
- Small status display
- 3D-printed modular enclosure
- Heat-set inserts and machine screws
- Strain relief and removable connectors

## Purchase rule

Do not buy the polished-control hardware until the software command layer is proven. Do not buy a Raspberry Pi or large touchscreen for V1 unless testing shows a real need.

## Electrical note

RJ-45 connectors on camera-control equipment must not be assumed to carry Ethernet. Connector pinout, signal type, and electrical levels must be verified from manufacturer documentation before any connection is made.
