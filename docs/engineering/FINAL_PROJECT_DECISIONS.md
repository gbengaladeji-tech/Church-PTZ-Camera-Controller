# Church PTZ Controller: final project decisions

Evidence checked 15 October 2026 UTC / 14 October in Toronto. **Start preliminary CAD now. Fabrication remains HOLD.** This file is the current specification. Proposed dimensions and untested functions remain clearly conditional.

## Frozen owner requirements

| Area | Current requirement |
|---|---|
| Enclosure | Sloped metal desktop console. Editable Onshape model. Screw-removable control panel, separately removable rear I/O and bottom service access. |
| Controls | 10 CAM + 12 preset + 12 technical buttons = **34**. Six rotary encoders. |
| Minimum illumination | 10 CAM + 12 presets + FAST/MIDDLE/SLOW + LOCK + AUTO FOCUS = **27 independent red LEDs**. |
| Technical inventory | STORE, FAST, MIDDLE, SLOW, LOCK, AUTO FOCUS, CAM OSD, ONE PUSH, MWB, ATW, IRIS and SHUTTER. |
| Preset layout | Four visual groups of three. P1-P12 always operate on the selected camera. |
| Joystick | ServoCity **605616**, retained. Pan/tilt plus twist zoom. No separate zoom keys or large STOP key. |
| Key appearance | APEM **1KC**, concave transparent lid, frosted-white diffuser, black 2K bezel, red illumination. Catalogued complete candidate **3FTH9871KC11162K09**. |
| Display | Owned **NX4024T032_011**. Exact suffix/revision and touch unverified. Operation must work without touch. |
| Connections | Four dedicated full-duplex RS-422 ports, plus separate Ethernet. CAM5-10 remain uncommissioned/disabled profiles. |
| Placement | AUTO FOCUS below the focus knob. No decorative grouping boxes are necessary. |

## Reference audit and unresolved owner decisions

The manufacturer-authored RMC-180 MARK II E4 manual, pp9-15, shows 32 keys: four CAM, sixteen presets and twelve technical keys. It has five dials, with shared menu/R-B functions and one shared iris/shutter dial. Retain the custom 34-key/six-encoder count; it is not an exact copy. The official site lists a newer E7 manual; the retrieved E4 is a dated reference, not asserted current.

Six provisional encoder assignments remain FOCUS, IRIS, SHUTTER, R GAIN, B GAIN and GAIN/MENU. Exposure gain differs from white-balance R/B gain, but its usefulness through this camera chain is not established. **Approve these assignments and IRIS/SHUTTER legends before engraving.** No extra button or encoder is added. The seven unlit technical keys can use seven of the 25 owned B3F-4050 switches, leaving 18 in stock. Caps are separate.

The selected PEC11R-N encoders have no push switches. Proposed non-touch settings workflow: hold CAM OSD to enter local settings with motion locked, rotate E6, use STORE to confirm locally, and CAM OSD to exit. No camera STORE command is sent in that mode. This requires owner approval and firmware implementation. RMC push-dial navigation and separate tally indicators are not silently added. Selected CAM means local selection, not on-air tally. AUTO FOCUS illumination will represent confirmed auto mode; the reference's red focus key indicates manual mode.

## Mechanical design basis

**Proposed:** 400 x 230 mm sloped surface, 10 degrees. Calculated body plan 400 x 226.506 mm, front height 55 mm, rear height 94.939 mm, excluding feet and protruding controls. The aperture band is 370 x 200 mm with 15 mm edge margins. The trial joystick hand allocation may approach within 10 mm of the side edge. The workbook contains all 42 named control centres and the world-coordinate transform.

A numerical 2D packing check found no intersections between the proposed envelopes. No ergonomic, native 3D interference or stiffness pass is claimed. Neither the old 350 x 180 nor 380 x 210 proposal was an accepted exterior dimension. A paper mockup and actual hand test can refine this new proposal.

Preferred quote: stock 5052-H32, 0.064 in = 1.6256 mm. Candidate tooling radius 0.062 in = 1.5748 mm, with 15 mm flanges. K-factor 0.38 and joint gap 0.5 mm are planning inputs. Supplier bend model, reliefs, seams, captive hardware and joystick reinforcement remain HOLD.

| Critical part | Verified reference | Fabrication hold |
|---|---|---|
| APEM 1KC | Cap 14.3 square; 2K bezel 17.75 square. Minimum family opening 14.7 square, uncoated. Drawing distinguishes 19.1 concave and 20.1 rim height references. | Exact switch/LED footprint, panel-to-PCB stack, retention and coated coupon. 19.1 is not below-panel depth. |
| ServoCity 605616 | Flange diameter 53.594; total height 85.09; four part holes diameter 2.54; Y pitch 32.512. | X pitch not independently dimensioned. The 39.116 ring is not an approved opening. Actual body/tabs, full sweep and hand clearance. M2 candidate; M3 does not fit nominal part holes. |
| Nextion | PCB 95 x 47.6; mounts 88.6 x 41.2, diameter 3.2. | Actual owned revision/window offsets. Official active widths 69.60 and 69.90 conflict. PCB outline is not screen opening. Mated connector depth. |
| Encoder/knob | PEC11R-4220F-N0024: M7 x 0.75 bushing, 6 mm shaft; nut/washer included. Knob 5527 diameter 20. | Knob page 12.5 mm versus drawing 15.5 mm overall. Finished panel/washer/nut/knob coupon; soldering method. |
| B3F/B32 | Bare switch body 12 square. B32 cap 12 square, reference assembled top 10 above PCB; uncoated opening 12.20. | Coated aperture, travel and separate support height. Trial 12.8 opening is not released. |
| W55RP20 | PCB 80 x 21; genuine STEP model envelope 85.35 x 21 x 16.6. | Received revision, sockets, plugs, brackets and jack alignment. Old W5500 board is not dimensionally interchangeable. |

Authentic W55 STEP was retrieved again and matches SHA256 `aa4aff49b0d9cc9ccaf8240ed07c0b269d2451c71db35f15d687fe0409b1663f`. Its package's CAD extracts are retained as reference; no new CAD-kernel or physical fit pass is claimed. Component sources and local hole patterns are in the dimensional workbook.

## Electrical corrections

Retain the 19-signal static pin allocation: UART0 GP0/1 CAM1, UART1 GP4/5 display, PIO GP6-11 CAM2-4, ADC GP26-28 joystick; GP2 shared clock, GP3 input load, GP12 input data, GP13 LED data, GP14 latch, GP15 global disable. No spare external GPIO. WIZnet's 13 October email confirms only GP0-15 and GP26-28 are available.

**46 inputs = 34 keys + 12 encoder phases:** six HC165 provide 48 bits, two spare. **27 LEDs:** four HC595 provide 32 bits, five spare; use 27 reviewed low-side sinks. The old twelve-LED/two-register design is obsolete. GP15 shares driver active-low enable and HC595 /OE. It must not be used for routine LED blanking/PWM. Receivers remain enabled. Registers operate at 3.3 V; LED current does not flow through HC595 outputs.

Conditional passive totals: 67 x 10k (46 input + 12 encoder filters + 9 boot defaults); 30 x 1k (3 ADC + 27 gates); 27 x 100k gate pulls; 27 LED limit resistors; 19 x 100nF including two conditional UART buffers and three ADC filters; 12 x 10nF encoder filters. Protection/regulator support parts are additional and unresolved. Trial 1.5k LED resistors at 5 V and assumed Vf=2 V give 54 mA total. Zero-Vf, 5.25 V and 1%-low resistance bound gives 95.5 mA. These are calculations, not LED ratings, brightness tests or approved resistor values.

WIZnet's Ethernet SDK also uses one PIO state machine and two DMA channels. Prior static allocation uses PIO1 SM0 Ethernet, SM1-3 camera TX, PIO0 SM0-2 camera RX, leaving SM3. DMA plan uses five channels, eight with optional camera TX DMA. No embedded build or coexistence pass exists. Forty-eight scan clocks at 250 kHz take 192 us, or 38.4% of a 2 kHz frame before software overhead. Load the final 32 LED bits before latching; qualify encoder missed edges and receive latency.

AM26LV31EIDR quad TX and AM26LV32EIDR quad RX remain conditional candidates. The receiver guarantees open-circuit fail-safe, not terminated-disconnected idle. Termination, bias, protection for all sixteen bus conductors, ground potential and possible isolation need review. Do not fit guessed resistor/TVS networks. Use a genuine four-wire full-duplex RS-422 bench adapter, not a two-wire RS-485 unit.

Board VSYS must remain 4.3-5.5 V after protection. Do not feed external power into USB VBUS. Joystick tracks use BOARD_3V3; separate AUX_3V3 powers the reviewed external circuit. Never parallel regulator outputs. The 5 V/3 A supply candidate has nominal margin over an illustrative 1.096 A allocation: 300 mA board + 500 mA display + 200 mA auxiliary + 96 mA LEDs. Actual load, inrush, fuse, thermal and USB arbitration remain untested.

## Camera functions and honest feedback

Datavideo documents 50 PTR-10T internal pan/tilt positions. Supplied manufacturer protocol V2.7 E4 documents set `8x 01 04 3F 01 pp FF` and recall `8x 01 04 3F 02 pp FF`, generic pp=0-127. The head's actual slot base/range and firmware still need qualification. Proposed P1-P12 to IDs 0-11 is **not a passed device mapping**. Test agreed spare slots without overwriting church presets. Lens/exposure recall is not established.

ACK means accepted. Protocol completion means executed; physical arrival semantics on the installed head remain unproven. Show REQUESTED/MOVING with red preset key. Only qualified arrival feedback permits REACHED and light off. Otherwise use COMMAND COMPLETE / ARRIVAL UNVERIFIED, or UNKNOWN on error/disconnect/timeout. A timer cannot prove arrival.

The emailed `912271.pdf` is a **non-T PTR-10 manual**, despite its email description. Its AG-CX350PX table lists zoom/focus. The T manual is separate evidence. Confirm actual camera variant, cable and PTR mode. Panasonic's public manual confirms only some functions through the 2.5 mm remote terminal. Iris, shutter, gain, WB/ATW, camera OSD and AF mode feedback remain disabled until qualified on the exact installed path.

STOP includes all relevant domains at the configured address: pan/tilt `81 01 06 01 01 01 03 03 FF`, zoom `81 01 04 07 00 FF`, focus `81 01 04 08 00 FF`. Earlier supplier shorthand called zoom STOP an all-axis stop and omitted a pan/tilt speed field; manufacturer format takes precedence. Neutral, LOCK, selection change and stale input require stop/re-arm logic. Power/cable loss can prevent STOP transmission; remote watchdog stopping is unverified. Test under supervision. Never parallel the RMC and custom line drivers.

## Cost, evidence and release

Current checked mechanical/power subset: seven caps C$4.13, six encoders C$21.06, six knobs C$28.26, joystick C$45.70, supply C$21.12 = **C$120.27 before HST/freight**, **C$135.91 with 13% HST**. APEM assemblies, unpriced electronics, AC cord, PCBs, freight and enclosure overage remain additional. Full remaining cost is **UNKNOWN**. Starting paper CAD costs C$0. An optional one-cap/encoder/knob/joystick fit basket is C$55.09 before tax/freight; adding the later PSU makes C$76.21. No purchases were made.

APEM sample/drawing/quantity-27 request was sent 14 October; no reply found. W55 sample is approved, owner confirmation sent, but no shipment/tracking/receipt found. ServoCity declined a discount. GMA originally offered twelve switches; owner reports 25 actually received. Protocase confirmed C$500 CAD support for fabrication, finish, graphics, hardware and shipping. Taxes/accepted quote are unresolved. End-of-week files improve the chance of November 6 delivery; that date is not guaranteed. Existing outreach is not duplicated.

Available/read evidence: attached brief, visible project context, draft PR2 including R6.3-R6.7, R6.2 machine-readable BOM and engineering notes/pinmap/protocol review, historical KiCad check JSONs, primary component drawings, supplier Gmail threads (APEM, GMA, WIZnet, ServoCity, Protocase, Applied Electronics, Datavideo, PCBWay). Panasonic-address search returned no messages. Full earlier project transcripts, original BOMv3 and separate earlier source files were not independently recovered. The package retains their inherited lineage, not a claim that every original was reread. No current native Onshape or revised KiCad model was accessible.

Historical KiCad D1 reports three unconnected nets and seven power ERC errors. No new KiCad run or corrected Gerbers are claimed. Existing Python tests cover simulation only; firmware/hardware, coupons, camera arrival and fail-safe tests remain NOT PERFORMED. No actual Onshape document, enclosure STEP or manufacturing drawing was generated; the guide and coordinate workbook define the work still required.

Superseded: R6.2 27 keys/12 indicators; R6.3 38 keys/16 presets; R6.6 1B 15.5 mm apertures; separate B3W/green LEDs/custom light guides; assumption all 25 donated switches must be installed. All 96 legacy BOM IDs are mapped once. The old mechanical MCU-01 labelled W55 while the BOM MCU-01 meant W5500; current W55 is MCU-02.

Friday preliminary DFM requires actual CAD exports with visible HOLD notes. Fabrication requires every critical fit/mount/clearance, owner layout/function approval, final quote and Protocase engineering acceptance. Work only on draft PR2's review branch; preserve firmware and historical files. No main merge or supplier message is authorized by this package.

## Primary references

- APEM cap/bezel drawing: https://www.apem.com/storage/datasheets/files/MEC_switches_serie_1K_1KB_1KC/media/MEC-switches-serie-1K-1KB-1KC.pdf
- ServoCity drawing gallery: https://www.servocity.com/3-function-joystick/
- Nextion family: https://nextion.tech/datasheets/nx4024t032/
- Bourns encoder: https://www.bourns.com/docs/product-datasheets/pec11r.pdf
- Datavideo protocol listing: https://datavideo.com/ap/protocol/181/ptr-10-mark-ii-visca-control-protocol
- Manufacturer-authored T manual, supplier mirror: https://files.hdtvsupply.com/datavideo-ptr-10t-mk-ii-um.pdf
- Manufacturer-authored RMC E4 reference: https://www.bhphotovideo.com/lit_files/846207.pdf
- Panasonic remote-control instructions: https://pro-av.panasonic.net/manual/html/AG-CX350P.PJ.EN.ED.AN.PX(DVQP1830ZA)_E/chapter08_01_02.htm
- W55 hardware: https://docs.wiznet.io/Product/Chip/MCU/W55RP20/w55rp20-evb-pico
- Protocase tooling: https://www.protocase.com/resources/bend-radii/
- Protocase finish guidance: https://www.protocase.com/resources/tolerances/finishes/
- CRA rates: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate/calculator.html
