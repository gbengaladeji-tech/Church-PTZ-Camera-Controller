# Controls and operator behavior

## Proposed 28-button map

The current front-panel count is exactly 28 Omron B3F-4050 switches:

| Positions | Labels | Firmware behavior |
|---|---|---|
| 1–10 | CAM 1…CAM 10 | Select one logical camera; CAM 5–10 reject by default because no route exists |
| 11–22 | PRESET 1…PRESET 12 | Recall on press; store when pressed while STORE is held |
| 23–25 | SLOW, MEDIUM, FAST | Select movement profile |
| 26 | AUTO FOCUS | Toggle automatic/manual focus only on a qualified route |
| 27 | AUTO IRIS | Show unavailable until exact supported behavior is verified |
| 28 | STORE | Modifier held while a preset button is pressed |

Every switch is debounced into separate `Pressed` and `Released` events. STORE
uses both; ordinary actions occur on press. Input loss clears STORE state so a
stale held flag cannot cause an accidental preset overwrite after recovery.

## Joystick

| Physical action | Default intent | Configurable items |
|---|---|---|
| X left/right | Pan left/right | minimum, center, maximum, dead zone, curve, reversal, max speed |
| Y forward/back | Tilt direction | same; direction must be confirmed by the owner |
| Twist | Wide/tele zoom | same plus zoom speed maximum |

The firmware will not arm until the joystick is valid and neutral. Each axis
inside its dead zone becomes zero immediately and requests the relevant stop.
Disconnected/invalid input stops active movement and enters `InputLost`.

Default speed maxima are deliberately conservative starting values inherited
from the prototype, not tuned physical-camera settings:

| Profile | Pan | Tilt | Variable zoom |
|---|---:|---:|---:|
| Slow | `0x04` | `0x04` | 2 |
| Medium | `0x09` | `0x09` | 4 |
| Fast | `0x12` | `0x12` | 7 |

Tune them on one supervised camera after the exact protocol ranges are checked.

## Encoders

- **FOCUS:** a detent requests a short near/far pulse. If autofocus is active,
  the controller requests manual focus first. A timer sends focus stop after the
  configured pulse. This remains capability-gated.
- **IRIS:** a detent requests one iris up/down command on a qualified route. The
  exact installed camera path must support it.
- **MENU:** changes a local display/settings value and must not directly send a
  camera command without an explicit menu action.

The decoder tracks the two-bit Gray-code sequence and emits a step only after a
complete quadrature cycle. An impossible two-bit jump resets the partial count.

## Proposed 13-LED map

The current software default uses LEDs 1–10 for the selected logical camera and
LEDs 11–13 for SLOW/MEDIUM/FAST. This is a proposed interpretation of the 13
separate red indicators and needs owner confirmation. They are separate LEDs,
not illuminated switches. Electrical current, driver stages, resistor values,
brightness, and physical light placement remain open.

## Nextion controls

No screen project/component IDs were found, so no page layout is claimed. A
future HMI should keep normal operation simple:

- home: selected camera, speed, connection/error state, focus/iris availability;
- settings: calibration, reversal, dead zones, curves, speed limits;
- diagnostics: raw ADC, debounced inputs, encoder counts, UART status, counters;
- error overlay: plain-language message plus the safe recovery action.

Touchscreen actions must use a documented page/component table and the same
controller methods as physical controls; they should not bypass safety state.
