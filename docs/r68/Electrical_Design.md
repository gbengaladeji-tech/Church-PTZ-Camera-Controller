# R6.8 electrical design specification

27 October 2026. Reviewable proposed topology, not a released schematic or PCB.

## Chosen partition and GPIO accounting

Three boards are the working recommendation: MAIN carries the W55 module, power/interface circuits and four rear camera jacks; KEY-L and KEY-R carry their local key/encoder circuits. Two boards would require one large, more expensive control PCB or many unsupported flying controls. A fourth rear carrier adds connectors, assembly and harness failure points. Integrating the rear jacks on MAIN avoids that cost only if real rear-panel placement and service clearance permit it. Actual board outlines, dimensions and cost comparison cannot be closed without the Onshape control centres and fabrication quotes.

Each key board gets three HC165 and two HC595. This uses six HC165 rather than the five-device theoretical minimum, giving two local 24-input banks with 14 spare inputs overall. It costs one extra input IC but permits local routing and identical scan/driver circuitry. The PCB shapes may still differ. This is not a claim that both boards already fit the real layout.

Signals: 8 camera TX/RX +2 display +3 ADC +5 shared scan/output bus +1 driver enable =19 GPIO. GP0-15 and GP26-28 are used exactly once. GP16-25 and29 remain untouched. In particular GP22 is unavailable. See Pin_Map.csv.

## Shared serial bus, exact bit order

GP10 clocks every HC165 CP and HC595 SHCP. HC165 clock inhibit is tied low, parallel load is GP11. The nearest 165 U1 QH connects to GP12. U2 QH connects to U1 DS; continue to U6, whose far-end DS is tied high. U1 is nearest the MCU and first sampled. Capture with CLK low, /PL low for at least the specified setup/pulse interval, then /PL high. Read H before the first rising clock, then G,F,E,D,C,B,A, then the next chip. Read all48 bits. Fit the short setup intervals and edge rate to the actual datasheet and cable length.

GP13 connects to nearest HC595 U7 SER; its QH' cascades to U8, then U9/U10. GP14 is the common output latch. For physical output bit n, use Q(n modulo8) on the appropriate chip. Shift physical bits31 down to0, then pulse the latch once. Every update sends32 bits; there is no partial-word shortcut. Input reads disturb only the hidden LED shift register. They must never pulse LED_LATCH. Conversely, after shifting lamps, recapture input data before reading it.

KEY-L uses input bits0-16 and LED bits0-12. KEY-R uses input bits24-40 and LED bits16-29. The CSVs define every slot, including spares. All HC inputs need defined levels, and all unassigned LED bits remain0. If actual controls must move between boards, update CSVs, firmware and tests together without changing the owner's visible layout.

## Key and LED circuits

For each contact: AUX3V3 ->10k pull-up ->input node ->momentary switch ->GND. Encoder common goes to GND and A/B to pulled-up inputs. The proposed10k value yields0.33mA per closed contact and11.22mA for34 closed contacts; confirm contact minimum load, noise and filter performance on samples. Long switch wires need conditioning/ESD review. Encoder edges use Gray-state decoding and error counts; button debounce must not block encoder acquisition.

For each LED: protected5V ->individual current resistor ->LED anode; LED cathode ->AO3400A drain; MOSFET source ->GND. A 595 output drives the gate through a provisional100ohm resistor, with100k gate-to-source pulldown. Verify the exact SOT23 pin numbering, low-Vgs performance and LED polarity before footprint release. The27 devices are separate sink channels, not a 27-LED load on logic outputs.

All595 VCC is3.3V. /SRCLR stays high; /OE may be tied low for this development topology. Outputs can be indeterminate at power-up before firmware shifts/latches zeros, so lamps may flash briefly. That behaviour must not be interpreted as READY. This design deliberately avoids tying LED /OE to RS enable. If boot-dark lamps become a requirement, add a separately validated power-on blanking solution; do not silently reuse GP15. Gate pulldowns alone do not guarantee darkness while a595 actively outputs HIGH.

Trial LED resistor820ohm1% at5V, Vf2V and negligible sink drop gives3.66mA. This is not a final rating. Recalculate at maximum supply, minimum Vf, resistor tolerance and verified allowed current, then measure legibility and resistor temperature. Conservative rail analysis also includes the hypothetical20mA-per-key case:27x20=540mA. Do not actually operate the keys at20mA unless their complete LED specification permits it.

## Joystick and screen

For each5k joystick potentiometer, connect its ends to MCU3V3/analog reference domain and AGND. Put the wiper through a provisional1k series resistor to GP26/27/28 and100nF to AGND near the ADC. Verify identification with resistance measurements, full-travel voltages and settling time. The three pots consume about1.98mA total at3.3V, calculated. Do not power them from the auxiliary regulator if doing so can overdrive an unpowered MCU. Disconnect/floating-wiper detection needs a validated network and tests; the host range guard is not sufficient to guarantee detection of every break.

The display is powered from protected5V, with GND common for this local UART. MCU GP4 TX ->screen RX only after screen VIH verification. Screen TX ->5V-tolerant3.3V input buffer ->GP5. Select a buffer with appropriate thresholds and partial-power-down behaviour, or design a divider with worst-case proof. Do not assume nominal5V input through a10k/20k divider is universally safe at tolerance and power-off. Exact buffer MPN and power sequencing are HOLD.

## Four camera interfaces

AM26LV31EIDR and AM26LV32EIDR are candidate SOIC16 devices on AUX3V3. Each camera has one independent driver and receiver channel; every camera port is point-to-point, full duplex. Follow the package-specific datasheet pinout rather than inventing pad numbers from a block diagram.

On the driver, tie active-low enable to3.3V and GP15 to active-high G, with an external10k pulldown on G. Driver output is high impedance when G=0 and /G=1. Set all serial TX lines to idleHIGH before raising G. Keep receiver enables independently defined for continuous replies; avoid tri-stated unpulled MCU inputs. Check power-off I/O injection between MCU and auxiliary rails. GP15 must not be shared with LED OE.

Logical port signals are1=reference,3=TX-,4=RX-,5=RX+,6=TX+,2/7/8=NC. Driver Y/noninverting goes TX+; Z/inverting goes TX-. Receiver A/noninverting is RX+ and B/inverting RX-. The reference head mapping is in Camera_Pinout_Reference.csv. The controller names and head names are opposite directions. View actual contact numbers from the jack/plug drawing, and continuity-test every cable before connection. This is a documented reference, not validation against installed PTR units.

Termination belongs at the receiving end of each transmission path, and must match cable impedance and existing head termination. Local RX options can be populated/DNP or selected, with values determined after inspection. Do not add another resistor blindly across a preterminated head input. A560/100/560 network gives0.270V nominal unloaded idle differential at3.3V with a100ohm terminator, but another termination or component tolerance can defeat it. Bias values remain HOLD pending worst-case analysis and actual cable/head tests. AM26LV32E open-circuit failsafe is not a guarantee for terminated shorted/idle lines.

Select port ESD/TVS with a complete common-mode and clamp-current analysis. Chassis/shield bonding is a site decision. This circuit is not galvanically isolated. If ground-potential or surge conditions require isolation, the new isolated transceivers and isolated supply must be designed and separately costed before church use. No isolation component is falsely included in the current budget.

## Power topology and provisional allocation

External certified5V adapter ->matched panel jack ->fuse/eFuse and reverse-polarity/overvoltage/inrush protection ->protected5V distribution. One branch feeds W55 VSYS using a board-schematic-verified backfeed arrangement; one feeds display; one feeds LED resistors; one feeds auxiliary3.3V conversion. Do not join the auxiliary output to the W55's3.3V output. Regulator and port protection MPNs remain open.

| Load | Provisional design allowance | Evidence class |
|---|---:|---|
| Nextion at5V |1.00A|Conservative allocation, not a measured/datasheet maximum|
| W55 board at5V |0.35A|Allocation pending measurement|
|27LEDs at20mA hypothetical |0.54A|Arithmetic, actual rating still required|
|Aux3.3V output |0.35A|Allocation for interface/logic; not additive as5V current|
|Aux equivalent5V input at4.75V/80%efficiency |0.304A|Calculated estimate|
|Total5V equivalent |2.194A|Conditional allocation|
|With25%margin |2.743A|Below3A only if allowances and losses are proved|

The3A adapter is a viable candidate, not a validated power budget. Startup/inrush, actual currents, thermal and cable droop must be measured. At5V->3.3V/0.35A, a linear regulator dissipates0.595W. A buck reduces heat but requires ripple/layout proof. RECOM R-78K3.3-0.5 has4.5V minimum input. At an adapter lower limit4.75V only0.25V remains for cable and protection losses before violating that minimum. RECOM was asked about this exact concern in the sent follow-up.

Until verified, service the board with external power physically disconnected when USB is connected. The board's internal diode/path must be reviewed before simultaneous supplies are allowed. Verify GPIO power sequencing and signal Ioff; disconnecting external power while USB remains can still energize some MCU outputs into unpowered peripherals. No camera cables during these tests.

## KiCad implementation and release checklist

- Create a new project revision; retain the old D1 archive as historical only. No native KiCad revision was completed here because the toolchain and final fit choices are missing.
- Add sheets for power, W55 sockets/service, scan/LED banks, joystick/display and four-channel line interface. Assign exact MPNs and package suffixes before footprints.
- Check each manufacturer symbol-pin-to-footprint-pad mapping, including jack mating view and MOSFET pin numbering.
- Name every rail/net, define all enables and unused inputs, add test points for5V, AUX3V3, module3V3, GND, DE, clocks/latch, UARTs and differential pairs.
- Create board outlines from actual mechanical datums, and mounting holes from measured support geometry. Add courtyard, case, cable, panel fastener and joystick motion keepouts.
- Support key boards for pressing loads. Separate return routing and local decoupling sensibly; do not split grounds blindly under digital return paths.
- Refill zones; run native `kicad-cli sch erc` and `kicad-cli pcb drc` using the installed version's help syntax. Save full reports and explain every intentional warning. Resolve the historical7ERC/3DRC findings in the new actual design.
- Cross-check schematic/PCB parity, print1:1 footprints, inspect3D, and have a reviewer check power and camera wiring. Export Gerbers/drills only after release gates close.

No ERC/DRC pass or manufacture-ready PCB is claimed in this package.
