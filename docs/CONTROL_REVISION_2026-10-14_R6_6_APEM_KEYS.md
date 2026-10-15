# R6.6 — APEM Multimec 1B Selected Button Family (14 October 2026)

**User decision:** select **APEM Multimec 5G + frosted-white 1B cap**, with a **red LED**, for the professional-looking illuminated buttons. Selection is of a **component FAMILY and appearance**, not a verified complete manufacturer ordering code or a paid purchasing authorization.

## Frozen controls (unchanged from R6.5)
- 10 illuminated CAM selectors; CAM1–4 wired, CAM5–10 uncommissioned future profiles.
- 12 illuminated preset recall keys in **four VISUAL banks of three** (P1–P12 refer to the selected CAM, not dedicated individual camera banks).
- 3 illuminated FAST / MIDDLE / SLOW keys, 1 illuminated LOCK and 1 illuminated AUTO FOCUS key.
- **Minimum 27 individually controllable illuminated keys**.
- Seven remaining ordinary controls may reuse the donated B3F-4050 (bare switches, **not caps**) with suitable panel tops and supports; the exact count of extra illuminated modes is not frozen.
- **34 physical buttons total**, six rotary encoders, ServoCity 605616 three-axis joystick, owned Nextion NX4024T032_011 (assume non-touch until verified).
- Sloped desktop controller, **screw-removable front control panel, removable rear I/O and bottom service access**.

## Manufacturer-specified 1B mechanical reference (not approved laser cutout)
- Visible 1B/2C/2D cap **15.1 mm × 15.1 mm**; manufacturer reference height **12.2 mm**.
- Specified nominal panel cutout **15.5 mm × 15.5 mm**.
- Long-travel rocker-action **2.0 mm**.
- Trial front-panel grid pitch **22 mm**; this is a project layout estimate, not an APEM requirement.
- Confirm 2C non-illuminated bezel vs 2D illuminated bezel, red LED type, key top diffusion, through-hole vs SMD, actuation force, flange capture, PCB-to-panel height and panel finish/tolerances before freezing CAD.
- APEM states not every code combination is stocked. An assembled frosted-white + red LED + suitable bezel **manufacturer part number is NOT YET VERIFIED**. **Do not order 27 switches from an assumed SKU.**

## Pricing
A Mouser Canada listing for **5GTH93582** shows a **red LED 5G switch core** at C$8.09 single and C$6.90 at qty 10; its actuation is 3.5N. This is not a quote for the chosen complete assembled 1B/2C kit: cap, bezel, accessories, freight and tax remain unresolved. Minimum 27 switch cores would be C$186.30 *if that same core is suitable and available at that volume*, before caps, bezels, PCB and shipping. Do not enter that illustrative amount as a verified committed BOM subtotal.

## CAD and electrical implications
1. Use **parametric placeholder** nominal 15.5×15.5 openings and 15.1 key tops in Onshape, with all such apertures tagged **HOLD — VERIFY ASSEMBLY AND FINISH**.
2. No manufacturing release until complete matched assembled key geometry/CAD file or one physical sample passes a coupon test, plus Protocase finish DFM.
3. 27 separately addressable LEDs materially exceed R6.2's 12-indicator approach. Recalculate LED supply, resistors/drivers, register outputs, board footprint and power budget without changing the provisional RP2040 GPIO plan blindly.
4. 7 unlit ordinary switches can be used only if cap heights and panel/PCB mounting are suitable; optionally choose matching non-illuminated APEM 1B caps to avoid visual mismatch if affordable.
5. Confirm control PCB dimensions, joystick mount and sweep, owned Nextion visible window, rear cutouts, screw/hardware mounting stacks, and manufacturable stock metal/bends.
6. Friday 16 Oct objective: **user-owned editable Onshape CAD + STEP + drawing + provisional DFM feedback request to Protocase**. Do not present an unverified panel cutout as production ready.

## Manufacturer sources
- APEM 1B family: https://www.apem.com/en-us/pcb-switches/mec-tactile-switches-and-accessories/1b-2c-2d
- APEM 1B/2C/2D datasheet: https://www.apem.com/storage/datasheets/files/MEC_switches_serie_1B_2C_2D/media/MEC-switches-serie-1B-2C-2D.pdf
- Candidate red LED 5G switch core (not complete assembly): https://www.mouser.ca/ProductDetail/Apem/5GTH93582
- Superseded control documents: R6.5, R6.4, R6.3 in docs directory.
