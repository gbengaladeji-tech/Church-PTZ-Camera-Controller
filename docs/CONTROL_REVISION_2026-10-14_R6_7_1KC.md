# R6.7 — APEM 1KC Concave Illuminated Key Selection

Owner confirmed on 2026-10-14 that the actual **APEM 1KC** concave transparent lid / frosted-white diffuser is the preferred appearance, replacing the previously selected 1B (R6.6). **This is the correct family for the next CAD revision.**

## Manufacturer part number (exact visual/electrical candidate)
**3FTH9871KC11162K09**
- APEM 1KC key top
- Frosted-white diffuser under transparent concave lid
- High-intensity **red** LED
- Black **2K bezel**
- Mounted on **3F through-hole tactile switch**, with user-insertable legend between lid and diffuser.
- Manufacturer catalogue source: https://www.apem.com/en-us/pcb-switches/mec-tactile-switches-and-accessories/1kc

Do not accidentally substitute similar-looking **1K**, **1KB**, **1KS**, or earlier **1B** codes, or the **1KC1116 cap by itself** for a fully functioning illuminated switch.

## Mechanical reference
- Visible cap footprint: 14.3 × 14.3 mm
- Full-family product reference height: 19.1 mm (confirm actual PCB datum / panel stack by drawing)
- Manufacturer nominal panel cutout: 14.7 × 14.7 mm; check coating/finish and supplier DFM tolerance
- 22 mm centre pitch is a **user layout proposal**, not a minimum manufacturer requirement; do not freeze final production openings without correct drawings or a fit-test sample.
- Supports a custom numbered/captioned legend insert in the cap.
- Manufacturer dimensional source: https://www.apem.com/storage/datasheets/files/MEC_switches_serie_1K_1KB_1KC/media/MEC-switches-serie-1K-1KB-1KC.pdf

## Pricing and supply gate
- Found **US$4.48 per unit for 1KC1116 cap alone** at Mouser (USD page; listing showed 0 stock in retrieved snapshot): https://www.mouser.com/ProductDetail/Apem/1KC1116
- This is **not** a complete 3FTH9871KC11162K09 quotation.
- **Total price / lead time / MOQ of exact assembled MPN: unverified.** Must get formal CAD quote or component bundle pricing before committing 27 units.
- APEM official MEC sample request: https://mktg.apem.com/en/mec
- Request **one verified complete sample** and **quantity-27 quote**, or educational project/sample support. Do not claim sponsor agreed or manufacturer committed.
- Previously donated 25 B3F-4050 remain for nonlit controls/testing; not the same mechanical assembly.

## UI / enclosure effect
- 10 illuminated CAM keys + 12 illuminated P1–P12 keys + illuminated FAST/MIDDLE/SLOW + LOCK + AF = **27 illuminated**, in **34 physical pushbuttons total**.
- Preset keys in four visual banks of three, function P1–P12 on the **selected camera**, not fixed camera groups.
- ServoCity 605616 joystick, Nextion NX4024T032_011, six encoders unchanged.
- User is making Onshape **screw-removable front panel + rear I/O panel** and serviceable sloped enclosure.
- Previous R6.6 **15.1 mm visible / 15.5 cutout belongs to the 1B family**, **must be superseded** with 1KC **14.3 visible / 14.7 nominal**.
- No finalized production CAD, LED-driver circuit, PCB footprints, purchase authorization, or real camera validation claimed.
