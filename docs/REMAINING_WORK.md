# Remaining work, in priority order

Do not skip a release gate because later work looks more exciting. Finish each
group's evidence before connecting production equipment.

## P0 — Resolve before schematic or camera transmission

- [ ] Physically identify the exact W55RP20 board revision/receipt and preserve
  clear photos of both sides and labels.
- [ ] Identify every installed PTR head and camera model, firmware, serial mode,
  controller settings, and known-good RMC cable.
- [ ] Obtain/read the exact Datavideo command and connector documentation with a
  working PDF extractor; create a source/page-backed command matrix.
- [ ] With all equipment powered off, continuity-map a known-good control cable
  and have the contact/polarity/common plan independently reviewed.
- [ ] Decide the five-serial-link architecture: proven UART+PIO allocation,
  external multi-UART, or reviewed switched-port bank.
- [ ] Prove its GPIO, PIO state-machine, IRQ/DMA, FIFO, and Ethernet resource
  budget before PCB release.
- [ ] Verify Nextion `_011` power/current/UART voltages and choose one-way level
  interfaces plus power-off protection.
- [ ] Select exact RS-422 transceivers, termination, failsafe bias, ESD,
  common/chassis reference, and any isolation.
- [ ] Complete the DC/USB power-path, fusing, reverse/backfeed protection, rail
  budgets, decoupling, and brownout plan.

Finish condition: reviewed schematic-level interface requirements with no TBD
pinout, voltage, or serial-resource assumptions.

## P1 — Production HAL and toolchain

- [ ] Install CMake, Arm GNU toolchain, Pico SDK, and exact W55RP20 board support.
- [ ] Cross-compile `ptz_commissioning`; archive full build log and size report.
- [ ] Define a proposed pin/resource table, then verify every alternate function
  against the exact board schematic/datasheet.
- [ ] Implement ADC sampler and calibration capture.
- [ ] Implement 40-bit input scan with documented button/encoder bit order.
- [ ] Implement 16-bit LED output with zero-before-enable startup.
- [ ] Implement Nextion nonblocking TX/RX queues and HMI layout contract.
- [ ] Implement the selected four-port transport with per-port RX framing,
  bounded queues, timestamps, errors, and loopback mode.
- [ ] Add persistent configuration with schema version, bounds, CRC, and safe
  defaults.
- [ ] Add watchdog only after reset/output behavior is proven.

Finish condition: embedded firmware builds, boots without TX glitches, and
passes subsystem tests with cameras disconnected.

## P2 — Bench electronics

- [ ] Confirm the exact 28 switches, three encoder suffixes/knobs, 13 LED MPNs,
  joystick, display, and connector parts actually in hand.
- [ ] Measure joystick terminal map, min/center/max, noise, direction, and
  open/disconnect behavior on all axes.
- [ ] Breadboard one button, one encoder, one LED sink, and scan-chain segment.
- [ ] Measure encoder edge capture during maximum turn and heavy serial/display
  load.
- [ ] Calculate and measure LED current/brightness and driver temperature; prove
  no reset/brownout flash.
- [ ] Run TTL UART loopback at the target baud, then a known-good full-duplex
  RS-422 loopback with unplug/replug, swapped-pair, missing-termination, and noise
  tests where safe.
- [ ] Measure all rails at idle/startup/worst case and all power-source
  combinations.

Finish condition: dated measurements and passing repeatable bench tests for each
electrical subsystem.

## P3 — HMI and control tuning

- [ ] Create the Nextion `.HMI` project and one source-of-truth component table.
- [ ] Implement home, settings, calibration, diagnostics, and error pages.
- [ ] Confirm the proposed 13-LED mapping (CAM 1–10 + speed 3) or change both
  docs and HAL mapping.
- [ ] Let the owner choose axis directions, curve, dead zone, and initial speed
  limits using recorded measurements.
- [ ] Define exact AUTO FOCUS and AUTO IRIS indicator/button behavior.
- [ ] Make unsupported features visibly unavailable.

Finish condition: display simulation and physical touch tests pass without
bypassing controller safety methods.

## P4 — One-head supervised commissioning

- [ ] Schedule a non-production test with authorization, safe access, another
  person observing, and the RMC-180 ready as fallback.
- [ ] Verify power-off cable continuity again and label controller/head ends.
- [ ] Power the custom controller without connecting the head; verify safe state
  and no unexpected TX bytes.
- [ ] Connect one head, select minimum speed, send one brief pan command, then
  stop and confirm ACK/completion/error bytes.
- [ ] Repeat opposite pan, tilt directions, neutral, input unplug, controller
  reset, and communication interruption.
- [ ] Test zoom only after pan/tilt/stop passes.
- [ ] Test one known safe preset recall, then store only with explicit approval.
- [ ] Qualify focus/iris/WB individually and update route capability flags from
  evidence; leave failures disabled.

Finish condition: signed/detailed one-head test log with zero unexplained motion
or electrical faults.

## P5 — Four ports, reliability, PCB, and enclosure

- [ ] Repeat commissioning on every port/head and under simultaneous display,
  encoder, input scan, and Ethernet traffic.
- [ ] Run long-duration neutral/movement/reconnect/reset soak tests and record
  all failures.
- [ ] Freeze schematic, bit order, pin map, connector/harness schedule, test
  points, PCB partition, and BOM.
- [ ] Run fresh ERC/DRC on the new design; older failed/obsolete boards are not
  manufacturing files.
- [ ] Fit-test real controls and connectors in coupons before releasing panel
  cutouts or PCB supports.
- [ ] Complete serviceable enclosure, strain relief, legends, grounding,
  fasteners, and thermal/current verification.
- [ ] Perform an independent code/electrical/mechanical safety review.

Finish condition: manufacturing package and release checklist refer only to
tested revisions and exact in-hand components.

## P6 — GitHub continuation

- [ ] Keep development on feature branches and require passing host tests.
- [ ] Add CI for the host C++ and Python tests.
- [ ] Add the embedded build after the toolchain is reproducible.
- [ ] Attach only public-safe test evidence; never publish addresses, private
  emails, discount codes, or unrelated personal notes.
- [ ] Update `DEVLOG.md`, `TESTING.md`, and the capability/wiring tables after
  every physical milestone.
