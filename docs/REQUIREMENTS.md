# Software and system requirements

Status words used here:

- **implemented** means host-testable code exists;
- **proposed** means the architecture supports it but hardware is not frozen;
- **blocked** means evidence or hardware validation is required;
- **unsupported** means firmware must visibly reject the function for that
  camera route.

## Operator behavior

1. The controller starts non-moving and ignores a displaced joystick until all
   three axes are valid and neutral.
2. Exactly one logical camera is selected at a time.
3. CAM 1–4 route to configurable physical transports. CAM 5–10 are disabled by
   default because the ten-to-four routing decision is unresolved.
4. Joystick X, Y, and twist request pan, tilt, and zoom with configurable
   calibration, filtering, dead zones, curves, limits, and direction reversal.
5. Returning an axis to its dead zone sends the appropriate stop without waiting
   for the smoothing filter to decay.
6. Slow, medium, and fast profiles limit pan, tilt, and zoom independently.
7. Preset buttons recall positions; holding STORE while pressing a preset stores
   that position only when the selected route declares preset support.
8. The focus encoder selects manual focus when necessary and sends a short
   near/far pulse followed by focus stop, only on a verified capable route.
9. Iris and white-balance commands remain unavailable unless the selected
   camera profile explicitly enables them.
10. AUTO IRIS remains unsupported until its exact target behavior is defined and
    verified. The UI must show unavailable rather than fake success.

## Inputs and output

- Debounce all 28 switches and produce separate press/release events.
- Decode direction from all three PEC11R quadrature encoders without applying a
  button-style debounce that discards valid edges.
- Define and test a complete shift-register bit order before PCB release.
- Process simultaneous actions deterministically. STORE plus PRESET is the
  defined store gesture; other buttons remain independent.
- Drive LEDs to a known-off state before enabling outputs.
- Use defined Nextion component IDs from a future HMI interface contract; do not
  scatter raw screen IDs through controller logic.

## Communications and safety

- Keep protocol encoding separate from physical UART/RS-422 transport.
- Validate all command inputs before packet construction.
- Track transport acceptance, VISCA ACK/completion/error, and response timeout.
- Stop active pan/tilt and zoom after 250 ms without fresh joystick input by
  default. This value is configurable and must be tuned during bench testing.
- Attempt a best-effort stop on shutdown, input loss, route change, and reply
  timeout. Never claim that a local attempt guarantees a remote stop.
- Avoid blocking the main event loop. UART receive, input scans, display updates,
  and timers must advance independently.
- Use a hardware watchdog in the final HAL only after its recovery/startup
  behavior has been tested.
- Recover from input loss only after a valid neutral sample. Recover from a
  transport fault through an explicit reset/reinitialization path.

## Display information

The future HMI must define component names/IDs for:

- selected logical camera and physical-route state;
- slow/medium/fast profile;
- ready, input-lost, transport-fault, and shutting-down states;
- unknown, waiting, acknowledged, online, timed-out, and protocol-error status;
- autofocus/manual-focus and capability-unavailable indicators;
- settings for calibration, dead zones, direction reversal, and speed limits;
- diagnostic counters and a concise last-error message.

No `.HMI` project or final component-ID table was found, so screen graphics and
page behavior are blocked. The testable serial protocol layer is implemented.

## Product and scope requirements

- Keep the four RS-422 camera connectors physically and visibly distinct from
  the W55RP20 Ethernet connector and label all rear ports clearly.
- Make the finished enclosure closed, strain-relieved, serviceable, and based on
  measured in-hand parts rather than concept dimensions.
- Keep CAM 5–10 disabled until a specific network protocol/profile and target
  have passed the same staged tests as a wired route.
- Preserve an immediate operator stop/recovery procedure and the original RMC
  controller as fallback during commissioning.
- Keep autonomous tracking, AI directing, automatic live switching, cloud
  services, and replacement of PTR motor electronics outside V1 scope.
- Document failures, test conditions, revisions, and operator feedback, not only
  successful demonstrations.

## Definition of software-ready for first bench test

- exact installed PTR model/mode and VISCA serial settings confirmed;
- one RS-422 channel pinout and electrical interface reviewed and continuity
  tested with power removed;
- W55RP20 pin/resource allocation proven under load;
- production transport/HAL implemented and its loopback tests pass;
- input calibration and neutral timeout pass on physical controls;
- low-speed move and stop packets rechecked against the exact Datavideo manual;
- an independent emergency power/control procedure and RMC fallback are ready;
- test is supervised on one disconnected/non-production head.
