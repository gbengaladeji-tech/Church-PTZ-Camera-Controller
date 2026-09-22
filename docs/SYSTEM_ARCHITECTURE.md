# System Architecture

## Current hybrid architecture

The current design replaces the earlier host-computer final architecture with an embedded RP2040/W5500 controller while preserving the useful software lessons from the Python prototype.

```text
Operator
  |
  +-- 3-axis joystick
  +-- CAM 1-10 buttons
  +-- preset controls
  +-- zoom / focus
  +-- speed / function controls
  +-- STOP / movement enable
  +-- status display
  |
  v
Input + state layer on RP2040
  |
  +-- debounce / input scanning
  +-- selected CAM/profile
  +-- movement state
  +-- speed state
  +-- preset state
  +-- safety state
  |
  v
Command layer
  |
  +-- existing VISCA command knowledge/test vectors
  +-- device/profile-specific command generation
  |
  v
Transport selection
  |
  +-------------------------------+
  |                               |
  v                               v
RS-422 transport              Ethernet transport
CAM 1-4                       future CAM 5-10
  |                               |
  v                               v
4 x Datavideo PTR-10/T        future verified
MARK II control links         DVIP/IP camera profiles
```

## Relationship to the existing Python software

The existing Python code is not discarded. It remains useful as:

- a protocol-learning record
- a known test harness
- a source of expected VISCA packet vectors
- a way to compare embedded output against previously tested behavior
- evidence of the software development process

The embedded firmware should reproduce only behavior that is understood and verified. The Python simulation must not be described as proof of real RS-422 communication.

## Camera/profile abstraction

The UI exposes CAM 1-10, but camera selection should be separated from transport details.

A camera/profile record should eventually contain:

- logical CAM number
- enabled/disabled state
- transport type
- physical RS-422 channel or network endpoint
- protocol/profile type
- capability flags
- preset behavior
- connection/status information

Initial mapping:

- CAM 1-4: physical RS-422 profiles
- CAM 5-10: unassigned/future network profiles

Selecting an unassigned profile must not transmit arbitrary commands.

## RS-422 transport

The final hardware provides four dedicated full-duplex RS-422 channels. Development sequence:

1. implement/verify one channel
2. bench-test the electrical interface
3. confirm pinout and PTR-10/T mode
4. perform one controlled real test
5. duplicate the proven design across the remaining three channels

## Ethernet transport

The W5500 provides one real wired Ethernet interface.

Its purpose is future expansion to compatible network-controlled cameras, including DVIP/IP workflows only where protocol support is officially verified.

The Ethernet implementation must not be presented as complete merely because the W5500 hardware exists.

## Design rule

Keep operator input, controller state, command generation, camera/profile capabilities, RS-422 transport, Ethernet/network transport, and user feedback/display as separate concerns.

## State that should be tracked

- selected CAM/profile
- profile enabled/disabled state
- transport type
- movement enabled/disabled
- pan speed
- tilt speed
- zoom/focus state
- active preset
- connection state
- last command
- error state

## Fail-safe behavior

On startup, reconnect, communication error, invalid input, unassigned CAM selection, or loss of input communication, the controller should prefer a stopped/non-moving state.

A dedicated operator STOP function must remain available independently of normal movement controls.