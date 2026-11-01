# Camera and display protocols

## Evidence boundary

The intended camera-control family is Sony-style serial VISCA as implemented by
Datavideo PTR-10/T MARK II heads. Datavideo's official product page lists Sony
VISCA and RS-422 and links the V2.7-E4 command reference. The repository also
contains a local copy of that PDF. The exact installed heads, firmware, serial
mode, camera/LANC path, and connector pinout still require verification.

The 2026 engineering handoff records 38400 baud, 8 data bits, no parity, one
stop bit as prior expert guidance for the PTR setup. It is not treated as a
universal VISCA default. Check the actual heads before transmission.

## Serial VISCA packet form

Commands in this project use:

```text
destination header | command bytes and parameters | FF
```

For camera address 1 the controller-to-camera header is `81`; address 2 is
`82`, and so on. `FF` terminates the message. The logical front-panel camera is
not necessarily the VISCA address: `CameraRouter` maps logical camera to a
physical port and address.

## Implemented packet builders

### Pan/tilt drive

```text
8x 01 06 01 VV WW PP TT FF
```

- `VV`: pan speed
- `WW`: tilt speed (a distinct required byte)
- `PP`: `01` left, `02` right, `03` horizontal stop
- `TT`: `01` up, `02` down, `03` vertical stop

Example: camera address 3, pan left and tilt up, speeds 4 and 9:

```text
83 01 06 01 04 09 01 01 FF
```

Stop is a pan/tilt-drive packet with both direction bytes `03`. Zoom stop is not
a substitute. The code defaults to generic VISCA maxima `0x18` pan and `0x14`
tilt, while speed profiles stop at `0x12`. Recheck the exact Datavideo limit
table before changing profiles or using the maxima on hardware.

### Zoom

```text
8x 01 04 07 ZZ FF
```

- `00`: stop
- `02`: standard tele
- `03`: standard wide
- `2p`: variable tele, speed `p` from 0–7
- `3p`: variable wide, speed `p` from 0–7

The original Python implemented fixed `02`/`03`. The new joystick path uses
variable `2p`/`3p` and tests the range.

### Presets/memory

```text
8x 01 04 3F 01 nn FF    store
8x 01 04 3F 02 nn FF    recall
```

The operator sees presets 1–50; `nn` is zero-based, so preset 5 is `04`. The
front panel exposes 12. Datavideo advertises 50 PTR-10 MARK II positions, but
store behavior and zoom-position support depend on the actual system and
accessories.

### Capability-gated camera commands

The encoder also contains common serial VISCA forms for:

| Function | Command body |
|---|---|
| Focus stop/far/near | `01 04 08 00/02/03` |
| Focus auto/manual | `01 04 38 02/03` |
| Iris reset/up/down | `01 04 0B 00/02/03` |
| White balance modes | `01 04 35 mode` |

These builders are testable protocol code, not proof that the installed
PTR/camera control chain supports the feature. Default routes do not enable
focus, iris, or white balance. Do not change capability flags until a controlled
test and command matrix say what the physical system actually does.

## Replies

The parser accepts the serial VISCA reply forms:

| Reply | Form | Meaning |
|---|---|---|
| ACK | `y0 4s FF` | command accepted in socket `s` |
| Completion | `y0 5s FF` | command finished |
| Error | `y0 6s ee FF` | command rejected/failed with error `ee` |

The controller records waiting, acknowledged, online, timed-out, protocol-error,
and transport-error states. The current transaction tracking is one outstanding
deadline at controller level; the final four-port transport should maintain
bounded per-port RX buffers and VISCA socket/transaction state under concurrent
traffic.

## Transport contract

`Transport::send(port, packet)` is intentionally small. The fake transport
records exact bytes in tests. A production implementation must:

- use the route's selected port only;
- configure the verified baud/framing;
- maintain TX idle correctly and avoid boot garbage;
- receive complete `FF`-terminated frames without blocking;
- bound all queues and report busy/disconnected/I/O errors;
- timestamp sends and replies;
- disable/reinitialize a failed route safely; and
- expose loopback diagnostics.

RS-422 is the electrical layer; VISCA is the message protocol. Passing a byte
unit test does not prove polarity, termination, or target compatibility.

## Nextion protocol layer

The display uses ASCII commands terminated by three `FF` bytes. For a future
component named `status.camera`, the layer can emit:

```text
status.camera.txt="CAM 2" FF FF FF
```

It also emits numeric `.val=` assignments and parses standard touch events:

```text
65 page component event FF FF FF
```

Component IDs and page numbers are not defined because no actual HMI project
was available. The code validates identifiers and rejects quotes, backslashes,
and control characters in text so display data cannot become another command.

## Primary sources

- [Datavideo PTR-10T MARK II VISCA protocol page](https://datavideo.com/us/protocol/182/ptr-10t-mark-ii-visca-control-protocol)
- [Datavideo PTR-10 MARK II product/download page](https://datavideo.com/global/product/PTR-10%2BMark%2BII)
