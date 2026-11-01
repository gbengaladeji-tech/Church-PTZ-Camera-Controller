# Original software recovery and engineering assessment

Assessment date: 2026-11-01 (America/Toronto)

## Recovery result

`software/controller_v1.py` is preserved without modification. Its SHA-256 is:

```text
ac3078564c2f2957bfe40a4fba7b832e16dbd1a832e4382655f2d70b77352c1d
```

The VS Code history record at
`/home/gbenga/.config/Code/User/History/-69ea2f4c/entries.json` contains 38
snapshots from 2026-08-25 15:52:25 to 19:26:13 EDT. The recovered file is
byte-for-byte identical to the newest recorded snapshot, `eLdw.py`.

The immediately preceding snapshot, `sH1Z.py` (18:57:58 EDT), is larger but
not a better revision: it contains two copies of the same packet functions and
an older one-shot preset demonstration before the keyboard loop. The final
snapshot removes that accidental duplication. Two intermediate snapshots have
syntax errors; later snapshots correct them.

The original VS Code history was read only. No file in it was edited, moved, or
deleted.

`git diff --check main...HEAD` reports trailing spaces on three speed-return
lines in this recovered file. They are original historical bytes and are kept
intentionally so the recovery hash remains exact; all newly written files pass
the whitespace check when this preserved artifact is excluded.

## What the prototype actually does

The prototype is a keyboard-driven packet generator. It remembers one of four
camera numbers and one of three speed modes, then prints hexadecimal byte lists
for:

- pan left/right, tilt up/down, and pan/tilt stop;
- fixed-speed zoom in, zoom out, and zoom stop;
- preset recall and preset storage; and
- camera and speed selection.

It uses the serial form of Sony VISCA implemented by Datavideo PTR-10/T MARK II
heads. For example, the prototype constructs pan/tilt drive as:

```text
8x 01 06 01 VV WW PP TT FF
```

`8x` is the addressed camera header, `VV` and `WW` are separate pan and tilt
speeds, `PP` and `TT` are direction bytes, and `FF` terminates the packet. Zoom
uses `8x 01 04 07 ZZ FF`; memory set/recall uses command `04 3F`.

## Communication correctness

The packet shapes implemented for pan/tilt, fixed zoom, and memory are
consistent with the project's Datavideo VISCA reference and the existing
learning notes. The prototype correctly includes separate pan-speed and
tilt-speed bytes and uses distinct stop commands for pan/tilt and zoom.

It is not, however, a communication implementation. `controller_v1.py` only
prints packets. The later `software/transport.py` is also explicitly
simulation-only. No code configures a UART, drives an RS-422 transceiver, reads
ACK/completion/error replies, enforces a reply timeout, or recovers from a
disconnection. A valid-looking printed packet therefore does not prove that a
PTR head will accept it.

Other correctness limitations are:

- camera headers, directions, zoom actions, and presets are not range checked;
- invalid helper inputs can return `None` and fail later with a less useful
  exception;
- preset numbers have no upper bound in the recovered file;
- the speed check uses the same 1–18 decimal range for both axes rather than a
  named, source-backed per-axis limit;
- movement continues at the camera until an explicit stop is delivered, but
  the loop has no input-loss watchdog or guaranteed shutdown stop;
- there is no acknowledgement/socket tracking, retry policy, or error state;
- global mutable state and the infinite input loop make the file hard to import
  and test; and
- camera addressing and physical port routing are treated as the same thing.

## Reusable work

The most valuable original ideas are the separation of normal operator actions
from protocol bytes, the camera/speed state, the packet examples, and the
keyboard/Arduino/Xbox test paths. They are useful as learning records,
regression examples, and host-side simulation tools.

The repository's later `software/ptz` package improves separation by defining
protocol-independent commands and a simulation transport. Its use of built-in
`unittest` is also reusable. It is intentionally incomplete and does not yet
encode VISCA packets.

## Implemented versus planned

| Area | Evidence-backed status before modernization |
|---|---|
| Camera selection 1–4 | Implemented in keyboard, Xbox, and Arduino/Python prototypes |
| Pan/tilt/stop packet generation | Implemented and simulated |
| Fixed zoom packet generation | Implemented and simulated |
| Three speed presets | Implemented with provisional values |
| Preset set/recall | Implemented and simulated |
| Analog joystick concept | Demonstrated through Xbox and Arduino input paths |
| Automated tests | Small assertion and `unittest` suites existed |
| Physical RS-422 transmission | Not implemented |
| Camera responses and status | Not implemented |
| Safe startup/input-loss stop | Not implemented |
| Focus, iris, and white balance | Planned only |
| Nextion display | Planned only |
| Button debounce and encoder decoding | Planned only |
| W55RP20 standalone firmware | Not implemented |
| Ten-position camera routing | Unresolved |
| Hardware-tested operation | Not performed or claimed |

## Rewrite boundary

The recovered file remains an immutable historical prototype. New firmware is
implemented separately so its validation, safety state machine, protocol
encoding, routing, and hardware abstraction can be tested without changing the
learning artifact. Python remains useful for simulation; production firmware
targets the W55RP20's RP2040 core using C++ and the Pico SDK.
