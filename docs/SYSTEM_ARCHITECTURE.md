# System Architecture

## Planned V1 architecture

```text
Operator
  |
  +-- joystick
  +-- camera buttons
  +-- preset buttons
  +-- zoom control
  +-- speed control
  +-- stop / movement enable
  |
  v
Input microcontroller
(Arduino-class device during prototyping)
  |
  v
Host control software
  |
  +-- input mapping
  +-- selected-camera state
  +-- preset logic
  +-- safety/state machine
  +-- VISCA command generation
  |
  v
Transport layer
  |
  +-- Simulation transport during development
  +-- RS-422 transport for real hardware later
  |
  v
Datavideo PTR-10/T MARK II
  |
  v
Panasonic camera + robotic head
```

## Design rule

The operator interface, command generation, and hardware transport should remain separate modules. This prevents UI or joystick changes from requiring the VISCA implementation to be rewritten and allows commands to be tested in simulation before real equipment is connected.

## Development stages

1. Keyboard -> simulated command output.
2. Automated command tests.
3. Arduino/input hardware -> simulated command output.
4. RS-422 transport development.
5. Controlled connection to one PTR-10/T.
6. Multi-camera selection.
7. Named presets.
8. Final physical console.

## State that should be tracked

- selected camera
- movement enabled/disabled
- pan speed
- tilt speed
- zoom state/speed
- active preset name
- connection state
- last command
- error state

## Fail-safe behavior

On startup, reconnect, communication error, invalid input, or loss of input-device communication, the software should prefer a stopped/non-moving state.
