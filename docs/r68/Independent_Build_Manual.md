# Church PTZ Controller: build and learning manual

R6.8 | 27 October 2026 | Design development, not manufacturing release

## 1. What you are building

Your controller is a small computer in a sloping metal enclosure. It reads an operator's controls, selects one of four wired camera ports, constructs a command, and transmits it to a Datavideo head. The head already contains the motors. The Panasonic camera receives only those remote functions supported by the installed head/camera combination.

The current panel has 28 pushbuttons: CAM 1-10, PRESET 1-12, SLOW/MIDDLE/FAST, AUTO FOCUS, AUTO IRIS and STORE. It has three encoders, a ServoCity 605616 spring-return three-axis joystick and the owned Nextion. There is no LOCK button. Twenty-seven buttons have red indicators; STORE can be unlit. The owner controls the appearance and existing Onshape layout.

CAM 1-4 select four separate RS-422 ports. CAM 5-10 must remain unavailable until an independently tested IP implementation exists. A real Ethernet socket on the W55 board is separate from the four camera sockets. Iris and autofocus controls remain unavailable unless the exact installed protocol proves support. Do not show a successful setting change merely because a dial turned.

## 2. Reading the status words

OWNED means the owner reports physical possession. APPROVED means a written offer exists. SHIPPED requires dispatch evidence; TRACKING requires an actual identifier; RECEIVED requires receipt. CAD RECEIVED means a drawing arrived, not a component. CANDIDATE means technically under consideration. QUOTE PENDING means no payable total exists. HOLD means a dimension, circuit or test is unresolved. VERIFIED must name what was verified: manufacturer data, computation, host test, actual measurement, or manufacturer approval. These are different kinds of evidence.

The owned Nextion and 25 bare Omron B3F-4050 switches are reported in the supplied handoff. Their physical dimensions were not measured in this run. WIZnet approved one W55RP20-EVB-PICO at US$0; the retrieved October 15 message promised tracking later. No tracking or receipt proof was found. Protocase confirmed C$500 manufacturing support and included shipping. PCBWay has not confirmed a monetary award. See the ledgers for every distinction.

## 3. Basic electricity in this controller

A voltage is an electrical potential difference between two points. A pin is a metal connection on a part. A pin labelled GND is the circuit's reference, not a licence to connect every cable shield arbitrarily. A 3.3 V GPIO normally communicates with voltages near 0 V and 3.3 V. A 5 V signal must not be assumed safe for that input.

Current is the rate of charge flow. A display may need hundreds of milliamps while a button contact carries a fraction of a milliamp. Add currents only when they are on the same rail. For a converter, compare power: input current is approximately output volts times output amps divided by input volts times efficiency.

Digital inputs distinguish states. A momentary button joins two contact pins while pressed. Wire one side to GND and the other to a 3.3 V pull-up and input; released reads 1, pressed reads 0. Confirm which legs are internally paired with the multimeter before soldering. A four-leg switch often contains two pairs, not four independent contacts.

Analog inputs measure a varying voltage. Each joystick potentiometer is a voltage divider: its two outer connections go to the MCU analog supply/reference and AGND, and its wiper goes to an ADC through a small filter. Power the pots from the MCU 3.3 V analog domain, never 5 V. The centre is approximately half supply but needs calibration. An unplugged wiper can look like a valid position; range checks alone are not wire-break proof. Add a validated fault-detection network or disconnection detection and test it.

An encoder is not a potentiometer. Its A and B contacts produce a Gray-code sequence such as 00, 01, 11, 10, 00. Reverse the order and the direction reverses. Read A/B quickly without applying long button debounce delays. Reject impossible two-bit jumps and count errors. The proposed scan target is 1 kHz, to be proved under simultaneous UART/PIO load; compare measured transition rates with this interval and increase it if edges are missed.

A shift register moves a group of bits through one data line. A 74HC165 captures eight contacts and then shifts them toward the MCU. A 74HC595 shifts an output word into a hidden register and transfers it to visible outputs only on its latch edge. Sharing their clock saves a GPIO, provided input captures and LED latches are scheduled correctly.

An LED needs current control. Its forward voltage is not a safe supply voltage specification. Each indicator gets its own resistor and transistor sink. A 595 drives transistor gates, not the LED load directly. With the proposed 5 V LED rail, resistor equals (maximum rail minus minimum LED voltage minus sink drop) divided by chosen current. An 820 ohm, 1% trial resistor gives roughly 3.6 mA at 5 V with a 2 V LED and small sink drop. This is a calculated trial, not a final brightness or manufacturer-current qualification.

UART is a serial byte interface. One wire transmits and one receives, with a shared reference. The Nextion uses a UART; confirm its actual TX level and use a verified 5 V-tolerant 3.3 V buffer or properly designed divider into MCU RX. A 10 k/20 k divider gives about 3.33 V from 5 V but its maximum tolerance, actual screen output, thresholds and power-off behaviour still need review. It is not an unconditional production solution.

RS-422 sends each direction on a differential pair. TX+ and TX- carry opposite sides of the same signal. RX+ and RX- receive a different pair. They are not four ordinary GPIO wires. The receiver detects the voltage difference, with limits on how far the whole pair may move relative to its reference. RS-422 is not galvanic isolation. Building-wide grounding may require isolated transceivers and isolated DC/DC power after a technician review.

The 8P8C jack is a connector shape. VISCA is a message protocol. RS-422 is the electrical signalling. Ethernet and HDBaseT may use similar connectors but are different interfaces. Label the camera ports `RS-422 CAM1` through `CAM4`; do not plug them into network switches or PoE.

A PCB is a manufactured board with copper connections. A footprint defines its pads, holes and mechanical outline for a particular component package. A good symbol with a wrong footprint still makes a bad PCB. Standoffs support a board at a specified height. They must establish the cap-to-panel height and resist repeated key pressure. The sheet-metal shell needs real support lips, fasteners and service clearances; it is not just a pretty outside surface.

## 4. Onshape: preserve the design first

Open the document with your existing controls. Open Versions and history and create a version before changing geometry. Versions preserve the model at that point; the working workspace remains editable. Rename existing features for recognition instead of rebuilding the control layout.

Measure a slope edge, then compare its length with the horizontal footprint. Use the supplied datum diagram. Define X across the panel, S along the slope and N normal outward. For the provisional 10 degree shell, world coordinates are X=X, Y=S cos(10)-N sin(10), Z=55+S sin(10)+N cos(10). N=0 is the exterior top; the panel lies at negative N. This avoids mixing vertical distances with normal-to-panel stack heights.

If the real top is 400 mm wide and 230 mm along the slope, the projected depth is 226.506 mm and the rise is 39.939 mm. The back height is 94.939 mm from a 55 mm front datum. If 230 mm is horizontal depth instead, the slope length is about 233.548 mm and back height about 95.555 mm. Do not constrain both inconsistent interpretations.

To add variables, use the Variable feature in the Part Studio and define `panel_w=400 mm`, `top_length=230 mm`, `slope=10 deg`, `front_h=55 mm`, `sheet_t=1.6256 mm` as working candidates. Reference existing dimensions where possible. Adding another driving dimension to an already constrained sketch causes conflicts. Use a reference/driven dimension when you only want to display a measurement.

Create a sketch on the real top plane. Use construction lines through datum A and actual mounting centres. For each control, make a named Mate connector or record X/S coordinates and axis orientation. Do not use arbitrary points on a cap surface when the true mounting datum is elsewhere. Fill the location CSV. Its empty fields are deliberate evidence gaps because the original document was unavailable here.

## 5. Onshape: build the serviceable shell

Use a formed bottom/front/left/right chassis, a removable sloping control panel and a removable rear plate as the preferred quotation topology. Protocase may favour separate side cheeks or a different bend order. Accept their stock/tooling advice before finalizing flat patterns. The reference STEP supplies an envelope study only; it deliberately has separate straight wall solids, no formed-corner development and no final holes.

Add a new Part Studio named `ENCLOSURE_CHASSIS`. Sketch the bottom rectangle in the horizontal plane using the measured exterior dimensions. Start Sheet Metal Model using the sketch/extrude method supported in your Onshape version. Set the candidate stock thickness and manufacturer-approved inside radius. Add the front and side flanges, then trim side profiles to the incline using supported sheet-metal cuts. Add rip/corner reliefs so sheet faces do not occupy the same material. If you instead sketch solid walls, conversion is successful only when Onshape produces a valid flat pattern with the intended bend/rip edges.

The historical process reference suggests 5052-H32 aluminum at 0.064 inch, radius about 1.575 mm and minimum flange about 7.62 mm. These are quotation candidates, not universal limits. A 12 mm inward top support is a useful starting envelope; its actual bend, screw access and hole-to-bend distances must satisfy Protocase's tools. Use eight provisional top fastener centres at X=12,200,388 on S=12 and218, plus X=12,388 at S=115 only if they do not collide with existing controls. All eight are HOLD and are omitted from the supplied blank DXF.

Support all perimeter edges, plus control boards where button forces demand it. Use approved captive/self-clinching hardware, attached brackets or standoffs rather than assuming screws can thread into 1.6 mm aluminum. A 10 mm provisional hole-centre exclusion from a bend tangent/edge can help initial packaging but is not a substitute for the selected hardware's edge and tooling rules. Ask Protocase to set the actual limits.

Make the rear plate a separate part inside the clear opening between sidewalls. Reserve four camera connectors, the W55's existing Ethernet/USB access and the DC inlet. Add edge protection where cables might touch metal, keyed harness plugs, a strain anchor near each external entry, and space to release connector latches. Four rubber feet go near the base corners, provisionally 20 mm in from each outer edge; choose screw length after measuring the foot and base.

Keep the bottom continuous unless top removal fails to expose a serviceable item. An extra hatch adds seams, screws and cost. Make every cable disconnectable before the top has to be pulled away. Add a service loop whose actual length permits safe opening, then retain it away from joystick motion. Do not let a loop fall into the mechanism.

Open Sheet metal table and Flat view and inspect bends, rips and reliefs. Right-click the real flat view to export its DXF. The package supplies only unbent blank-panel outlines and labels them explicitly. It does not claim a chassis unfolding. Paint, bend compensation and production tolerances belong to the accepted manufacturer's process, not guessed K-factors.

## 6. Fit the actual components

For APEM 3FTH9871KC11162K09, the current manufacturer page identifies through-hole mounting, 1KC cap, 2K bezel and high-intensity red LED. It lists a 14.3 mm square face, 19.1 mm height and 14.7 mm nominal panel opening. The recovered `1KC.stp` contains three solids with a combined bounding box about 14.449 x14.449 x12.493 mm; `1KC1116.stp` is one 14.3 x14.3 x12.5 mm solid. Those bounds are not 19.1 mm and do not prove the full switch/LED/PCB stack. Keep both files as real references, not an invented complete switch assembly.

Test one complete APEM assembly in a coupon made with the final thickness, finish and PCB standoff. If coat thickness per edge is c, nominal raw opening starts at finished opening plus 2c; add process tolerance and required running clearance, then obtain manufacturer agreement. For illustrative coating of 0.076 to0.127 mm per edge, 14.7+2c is 14.852 to14.954 mm before further tolerance. Do not turn that example into a production cut.

The owned B3F-4050 cannot directly accept a 1KC cap. STORE therefore stays a mechanical decision: use a separate supported cap/adapter and verify appearance, or request an extra matching APEM assembly with separate funding. Do not quietly order a mismatched part or assume 25 donated switches solve 27 illuminated keys.

ServoCity's 605616 has three 5 k potentiometers and spring return on all axes. The manufacturer page gives 50 degree X/Y travel and solder tabs. Keep the historical flange and one-axis pitch as references only. Obtain the second pitch, centre cutout, mounting screws and full swept volume from the complete drawing/sample. Do not turn the listed flange or inner diameter into a panel hole. Check the full left/right/up/down/twist hand motion with the 100 mm construction clearance circle and adjacent knobs.

The PEC11R-4220F-N0024 is a 24-pulse/24-detent, no-push-switch encoder with a 6 mm flatted shaft and M7x0.75 bushing. Confirm nut/washer, antirotation features, panel thickness and knob engagement. The 5 V contact-rating listing does not mean the contacts require a 5 V supply: scan passive contacts at 3.3 V. A Cliff 16 mm matching D-shaft knob was suggested in the actual email; its appearance and fit are an alternative, not an approved substitution for the selected black knob.

The Nextion family dimensions in the recovered data are 95x47.6 mm PCB and mounting-hole centres 88.6x41.2 mm with 3.2 mm holes. The screen-region 69.60 versus69.90 mm discrepancy remains unresolved. Read the rear suffix and revision, check touch operation, measure the visible border and cable. The screen window must expose the intended region and hide/support the rest of the module. Leave clearance for installation without scraping the glass.

Use the recovered authentic W55 STEP to check Ethernet, USB and header plugs, not just the 80x21 mm PCB. It does not prove the sample revision or delivery. Keep BOOTSEL, RUN and SWD accessible after assembly. Add real connector models and plugged-in cable envelopes before drilling the rear plate.

## 7. Assembly and inspection in Onshape

Create an Assembly tab, insert the chassis and fix it at the origin. Insert the top and rear panel. Create Fastened mates between explicit chassis and panel Mate connectors; choose connector origins from actual mounting datums and check axis flips/offsets. Insert one real key assembly, mate it to its control datum, then reuse the component with patterns or repeated Fastened mates. Keep existing visual patterns until replacements are verified. Do not drag parts until they look approximately right.

Insert the planned boards only after board outlines and mounting hole origins exist. The working electrical partition is three boards: MAIN, KEY-L and KEY-R, with rear jacks on MAIN to avoid a fourth carrier and harness. Each key board has three HC165 and two HC595, allowing 24 inputs and16 output slots locally. Six HC165 cost one more IC than the theoretical minimum but permit symmetrical local scan electronics, fewer long individual wires and14 spare contacts. This is a concrete electrical recommendation; PCB shapes and whether MAIN can physically reach the rear plate remain HOLD until the real control coordinates exist. If this partition cannot support the actual layout, revise it and re-quote before release.

Make section views at the joystick, screen, key PCB, encoder bushing and rear jacks. Record minimum clearances including metal tolerance, board warp, screw ends and wire bends. Use 3 mm static/5 mm moving-wire clearance as provisional design targets only, increased where the real component requires it. A chosen target is not a measured result. Check panel extraction with boards attached and all plugs installed. Finish only when you can remove the top, rear and each serviceable board without forced bending or hidden screws.

Create drawings with top ordinate positions, side slope/heights, rear connector view, underside supports and a section showing the panel-to-PCB stack. Put revision, material, finish, datum, tolerance notes and every HOLD on the drawing. Preliminary reference files can be sent for DFM, but only a manufacturer-accepted production revision should be fabricated.

## 8. Electronics and wiring sequence

Use `03_electrical/Pin_Map.csv`, `Input_Map.csv`, `LED_Map.csv`, `Harness_Schedule.csv` and `Electrical_Design.md`. The standalone GPIO map uses GP0-15 and GP26-28 only. GP22 is internally occupied and must never be used. GP15 solely controls transmitter enable; it is not shared with LED OE. Shared GP10 clocks both chains; GP11 captures inputs, GP12 reads them, GP13 shifts LED data and GP14 latches lamps. Display uses UART1 GP4/5, camera1 UART0 GP0/1, and three experimental PIO TX/RX pairs use GP2/3,6/7,8/9.

All HC logic runs at3.3 V. Do not power HC595 at5 V and assume 3.3 V is a guaranteed HIGH. Each IC gets a nearby100 nF ceramic capacitor; select exact capacitor MPN, voltage rating, dielectric and footprint before BOM release. Input contacts use10 k pull-ups to3.3 V as an initial design value. At34 simultaneously closed contacts that is11.22 mA, calculated. Encoder phases use validated conditioning and state decoding rather than long blocking debounce.

For the proposed TI driver, tie active-low enable high and use GP15 on active-high G with a physical10 k pulldown. That combination disables transmitters at reset. Keep UART TX high before enabling the driver. Receiver enable is independent and its MCU outputs require power-sequencing review. Receiver open-input failsafe does not guarantee a terminated, shorted or noisy pair reads idle; termination and bias must be designed for actual cable/head conditions.

At each receiving end, fit termination matching the cable and existing head network, not both ends of every direction automatically. Provide selectable/DNP resistor footprints. A historical560/100/560 bias proposal yields about0.270 V nominal at3.3 V, but tolerances and a possible second terminator can destroy that margin. It is not released. Select ESD/TVS based on actual common-mode limits, clamping voltage/capacitance and surge/grounding assessment. The IC's own ESD rating does not certify the finished port.

Use a certified external5 V adapter. The candidate GST18U05-P1J needs the correct wall lead if not included and the correct mating jack geometry, polarity/current rating and panel nut stack. Fuse/current-limit and reverse-polarity protect the entry. Do not assume a generic5 V TVS clamps below a5.5 V MCU supply limit; evaluate an overvoltage-protected eFuse/load switch. Keep external supply and USB from backfeeding each other with a verified power path or physically disconnect external power during USB service. A blanket instruction to connect both to VSYS is insufficient until the board schematic is reviewed.

Use a separate3.3 V auxiliary rail for line devices/logic, and the W55 analog supply only for the three joystick dividers. Never join two independent3.3 V regulator outputs. The RECOM R-78K3.3-0.5 is a candidate with4.5 V minimum input and0.5 A output. Allow for all upstream losses; the protected rail must remain above its minimum. The 5 V-output R-78K variant cannot regulate5 V from a5 V input because its minimum is6.5 V. A linear regulator at0.35 A would dissipate roughly0.595 W from5 V to3.3 V, requiring thermal proof.

## 9. Understand an operator action

Press CAM2. A contact changes from1 to0. The scan chain captures it; debounce recognises one press. The controller first sends pan/tilt, zoom and focus STOP requests to the old port, then changes selected port to2 and disarms until neutral and confirmed rest. The CAM2 indicator means selected, not that the physical head is connected or has reached a shot. Initial rearming during qualification uses a deliberate service/technician action, not a hidden automatic motion restart or a resurrected LOCK button.

Move left after qualification. The ADC reports an offset from calibrated centre. The controller applies deadband and bounded speed, routes bytes to port2, and ordinarily uses device address1 on that independent cable. Selecting CAM2 must not automatically mean VISCA address2. This differs from the old legacy Python examples and is tested in the new reference core.

Release the joystick. Send a specific pan/tilt STOP and separate zoom/focus stops where applicable. A motion command can persist at the head after the MCU stops transmitting. Hardware disable, watchdog reset or loss of power can prevent the STOP message from arriving. Confirm actual head behaviour during supervised failure tests. Keep motion areas clear and retain the existing controller as fallback.

Press PRESET4. It means selected camera's preset4, not camera4. Firmware may show `Recall sent`, then `Acknowledged`; only matching, validated completion/position evidence can show `Reached`. A timeout shows unknown/error. The zero-based mapping P1->0 is provisional and must be checked against installed firmware. STORE must require a deliberate confirmed operation to avoid accidentally overwriting presets; the supplied diagnostics do not write presets.

## 10. Firmware work you can do offline

The package contains a pure Python reference safety core plus13 new automated tests. Together with the existing four command tests,17 unit tests passed; the legacy assertion script also passed. These prove only the stated host behaviours. The old files remain unchanged. Do not use their old camera-number/header assumption as a production routing rule.

With Python3.10 or later, open a terminal in the included `software` folder, run `python3 -m unittest discover -s tests -v`, then `python3 test_controller.py`. Read a test, explain its expected failure scenario aloud, then change an input to see the guard reject it. Avoid memorising packet arrays without understanding port, address, action and response.

The `firmware/r68/diagnostic.py` code targets MicroPython on the W55 RP2040 and keeps driver enable LOW. It reads48 input bits and three ADC channels; it can write an LED mask after the wiring/LED resistor review. It was syntax-checked on the host, not executed on the board. Do not connect camera cables. Copy `pins.py` and `diagnostic.py` together onto a suitable board only after checking the exact firmware/board revision. Run it manually from the REPL rather than adding automatic boot behaviour.

`pio_uart.py` is an experimental8N1 loopback transport. It uses six state machines; it does not provide a production response parser, queue arbitration, framing-error reporting, watchdog integration or a complete operator loop. It must pass logic-analyser tests at38400 baud under input/display/Ethernet load before being used with the head. A production binary or hardware-tested W55 controller firmware has not been produced.

A fault must latch disarmed, send a bounded high-priority STOP bundle where transmission is still possible, report unknown rest and require deliberate rearm after neutral. Do not discard queued STOP requests by disabling the driver before the UART/PIO has physically sent the final stop bit. On an event-loop hang, the watchdog can reset local hardware but cannot guarantee a remote stop. Normal packet queues must not delay emergency STOP traffic.

## 11. Bench and commissioning tests

First, with no power, check GND versus supply resistance, connector orientation and lack of shorts. Map actual jack contact numbers from the mating view and prove cable continuity with a meter. Generic plug colours are insufficient evidence.

Power only the protected entry and verify polarity and voltage before inserting electronics. Then add auxiliary regulator, MCU, one input chip, one LED sink, screen and joystick in stages. Record supply current and any temperature rise. Never connect an Uno5 V TX directly to W55 GPIO. The existing Arduino kit can demonstrate buttons/encoders independently, but that is not a W55 electrical qualification.

Perform a walking1/0 scan-chain test across48 slots and a one-lamp-at-a-time test across all27 assigned outputs. Spares stay off. Verify simultaneous button presses, encoder reversals/bounce, display corruption, ADC unplug/out-of-range, boot/reset and power sequencing. Use a scope/logic analyser or a technician's equipment to validate3.3 V UART and differential signal quality; a multimeter cannot show serial timing.

Loop back TX/RX through one driver/receiver pair on a test cable. Check38400 8N1, idle polarity, termination, negative/positive mapping, reply capture and errors. Stress all four channels together. Test USB-only and external-only service cases and verify no backfeed. Never use powered church equipment as the first electronics test load.

With church technician permission, use one disconnected/supervised head outside services. Confirm exact model, firmware, DIP mode, cable, address and baud. Start at minimum speed. Check pan/tilt/zoom/focus separately, three-domain STOP, neutral, camera switch, cable unplug, power interruption and recovery. Record expected/actual outcomes. Do not assert iris or autofocus support without proof. Repeat for four heads only after one passes. Qualify any Ethernet capability later as a separate revision.

## 12. Purchasing, support and final release

Do not order a pile of inexpensive parts before solving the expensive keys. Live retrieved prices cover a few items only; the complete delivered total is unknown. The retail base-switch benchmark alone fails the cash cap. A donated screen or enclosure credit cannot be subtracted twice or transferred to another category.

Ask for a complete quote listing exact MPN, quantity, included accessories, currency, tax, freight, brokerage, duties, lead time, quote expiry and sample conditions. Reconcile it using the budget calculator. Unknown costs must keep checkout on HOLD. Never count PCBWay/MEAN WELL possible support as funded. Do not add unwanted parts to reach a shipping threshold without comparing the real delivered totals.

Protocase may review a preliminary shell before all holes are resolved. A useful DFM request identifies the approximate envelope, removable panels, working stock, support topology, finish and unresolved fit items. The reference STEP and PDF in this package are honestly labelled concept-only; they are not exports of your current Onshape control layout. A final production quote needs the completed integrated model.

Finish this project through recorded evidence, not a calendar promise. Freeze one revision, close each risk, get a manufacturer-accepted quote and drawings, rerun native KiCad ERC/DRC, build/test the actual hardware and obtain church acceptance. The original November6 target and requested November30 revision are not verified delivery commitments.

## 13. Source index and access limits

`06_evidence/Source_Register.csv` lists actual recovered documents, original-mail IDs and authoritative web URLs. The two supplied October27 Markdown files are the latest owner baseline. R6.7 and older workbooks are historical engineering references and contain superseded counts. Current source access recovered the BOM release, dimensional workbook, outreach workbook, risk register, R6.6 tracker, R6.7 Markdown, R6.2 archive and real component STEP files. Therefore those files are not labelled expired.

Full project conversation transcripts, original current Onshape workspace/screenshots, a live complete quote, physical measurements, manufacturer production acceptance and a current native KiCad toolchain were unavailable. A project-memory summary is not a full conversation read. Email searches recovered relevant threads and bounce notices, but broad searches returned result caps and exact-mailbox history was used for actual follow-ups. This is not a claim to have read every message in the account. No new-company prospect is labelled never-contacted without an exact domain/group check.

Current primary references include APEM's exact assembly page, ServoCity's605616 page, Bourns PEC11R datasheet, WIZnet's board documentation, TI's line-driver/receiver and HC logic data, RECOM's regulator data and Onshape's current sheet-metal/export/Fastened-mate help. The source register also records vendor price pages as retail snapshots. Physical samples and accepted drawings remain the final fit evidence.
