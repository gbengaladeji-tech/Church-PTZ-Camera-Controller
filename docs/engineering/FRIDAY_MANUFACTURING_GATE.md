# Friday 16 October 2026: manufacturing gate

**Ready to start preliminary CAD. Not ready for fabrication.** The dimension schedule and build guide exist. A complete preliminary DFM package still requires creating the actual Onshape model and exporting its STEP and dimensioned PDF.

## Preliminary DFM handoff

Use `PRELIMINARY DFM - NOT FOR FABRICATION` on the drawing and export revision. The owner reviews the proposal before submitting. No supplier email was sent during this audit.

- [ ] Create editable Onshape geometry with all 34 keys, six encoders, display and joystick, plus removable top, rear and bottom access.
- [ ] Export complete assembly STEP in mm and dimensioned PDF exterior, control, rear and section views. Identify every HOLD aperture/mount. Do not offer an unverified flat pattern as approved.
- [ ] Include the editable CAD review link, matching revision, coordinate schedule and this gate file.
- [ ] Specify quantity1, stock 5052-H32 /0.064 in candidate, economical finish, stock hardware and proposed legends.
- [ ] Ask Protocase to review construction, tooling access, seams, stiffening, aperture finish allowance, quote and schedule. Request DFM feedback, not fabrication while holds remain.

Protocase's22 September email accepts STEP plus dimensioned PDF; SolidWorks Pack and Go is preferred. Its23 September email confirms C$500 CAD support covering manufacturing, finish, graphics, hardware and shipping. Taxes are not addressed. Its12 October reply recommends final files by the end of the week for a reasonable chance of November6 delivery. There is no guaranteed delivery, accepted quote or tax waiver.

## Fabrication blockers

| Gate | Evidence needed | Owner | Current state |
|---|---|---|---|
| G1: APEM complete assembly | Quote/MOQ/lead time; assembly drawing/footprint and PCB-to-panel stack; finished coupon | APEM + owner | OPEN |
| G2: 605616 joystick | Measure both hole pitches and actual opening; moving and hand sweep; tabs and wire exit | Owner / ServoCity | OPEN |
| G3: Owned Nextion | Rear-label suffix/revision; window offsets; hole pattern and mated cable depth | Owner | OPEN |
| G4: Seven B3F/B32 + six encoder/knobs | Coated coupon, cap travel, knob engagement and all standoff heights; soldering method | Owner / assembler | OPEN |
| G5: Full layout and functions | Approve42 control centres (34keys+6enc+display+joystick), proposed 400x230 surface and labels; six encoder/mode mapping | Owner | OPEN |
| G6: Rear I/O and power | Exact LAN/DC/USB openings, connector orientation, fastening, PCB brackets and cable withdrawal | Electrical + CAD | OPEN |
| G7: Board supports and interference | Native PCBs or bracket design; mounting grid; full3D interference and lift-out/strain relief test | PCB + CAD | OPEN |
| G8: Sheet-metal DFM and quote | Stock material/radius/fasteners; seam/finish tolerances, joystick load path, quote and owner approval | Protocase + owner | OPEN |

## Fabrication release requires every applicable condition

- [ ] Owner approves all control positions, six encoder assignments, mode legends, angle and dimensions.
- [ ] Exact critical apertures, mounting patterns and connector views match the received component revision or recorded measurements with tolerances.
- [ ] Finished-panel coupons pass complete APEM, B3F/B32, encoder/knob and rear-jack stacks, including travel and retention.
- [ ] Both joystick mounting pitches, actual opening, body/tabs, hand and moving sweeps are verified. The display window offset and mated cable fit are checked.
- [ ] PCB/bracket drawings, mounting interfaces, native3D interference, lift-out, cable routing and screw access are checked. Panel stiffness and joystick load paths pass review.
- [ ] Protocase accepts tooling, bends, reliefs, tolerances, seams, finish and stock fasteners. Final drawings identify no unresolved production feature.
- [ ] Final quote, sponsorship eligibility/credit, tax, shipping and timing are reviewed. Owner authorizes fabrication.

Firmware development does not prevent an exterior DFM discussion. It can affect power, connectors and PCB mechanics; those interfaces must be resolved before their features are fabricated. Actual camera validation is a separate commissioning gate.

## Shortest practical sequence

**Thursday15 October:** measure the owned Nextion label/window/connector. Get the already-requested APEM assembly drawing or sample; do not duplicate outreach. Obtain an owner-approved minimal fit set if needed. Verify both joystick pitches and hand reach with a100%-scale paper layout. Small printed coupons can use the owned A1Mini; the full metal enclosure need not fit its180 mm bed.

**Friday16 October:** create Onshape geometry from the schedule, derive supports and cable volumes, review orientation and quantities, export actual STEP plus PDF. Submit for preliminary DFM if any critical dimension is still open. Missing physical geometry is not resolved by a deadline. A blank-panel/inserts alternative needs a separately verified strategy and owner/Protocase agreement; it is not preapproved here.

**Afterward:** finish protected power and line-interface design; update native KiCad for46 inputs,27 LEDs and19 GPIO; close historical ERC/DRC; prototype one RS-422 channel; qualify camera functions, safe spare preset slots and STOP/arrival feedback; expand to four channels under display/encoder/Ethernet load; complete commissioning. Do not overwrite production presets during tests without an agreed slot plan.
