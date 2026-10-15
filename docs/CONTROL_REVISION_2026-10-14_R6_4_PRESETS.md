# R6.4 — 12 Illuminated Presets and Datavideo-Style Keys
**Owner decision:** 14 October 2026. **Authority:** supersedes the 16-preset / 38-button estimate in R6.3.

## Frozen quantities
- **10** illuminated physical CAM selector buttons (CAM1–4 planned wired; CAM5–10 profiles disabled until connection proven).
- **12** illuminated physical preset buttons (reduced from 16).
- **12** technical/mode pushbuttons (STORE ×1, FAST/MIDDLE/SLOW ×3, LOCK ×1, AUTO/MANUAL FOCUS ×1, CAM OSD ×1, ONE PUSH/MWB/ATW ×3, IRIS/SHUTTER ×2).
- **34 total pushbuttons**, **six rotary encoders** remain planned and **ServoCity 605616** fixed.
- Bare, donated Omron **B3F-4050 ×25** are neither complete panel caps nor integrated-LED assemblies; only use in non-illuminated positions where the mechanical cap and PCB-to-panel stack is explicitly checked.
- Integrated illumination needed **at least 24 positions**: 10 CAM + 12 PRESET + LOCK + AUTO FOCUS. Other technical modes may need more; final LED channel count and drivers are OPEN.
- These changes invalidate R6.2's 27-button/12-indicator and R6.3's 38-button/control PCB layout as final ordering quantities.

## Visual target
Datavideo RMC-180 MARK II inspired: broad, milky/translucent white, nearly square, slightly rounded key tops; close, regular spacing; RED illuminated active key. Match the feel and proportions without assuming the RMC's proprietary components are available or making counterfeit branding.
**Do not freeze front-panel cutouts** until an exact purchasable illuminated assembly (body + actuation travel + built-in LED + mating PCB and support height) and mounting drawings have been confirmed.

## Preset state behavior — desired, NOT proven
1. Inactive: unlit or softly white key (whether a second color needs an LED is TBD).
2. When recall command is initiated: selected preset key **red while the move is in progress**; display indicates `MOVING TO PRESET #`.
3. When arrival has been **verified by actual device completion/position feedback**: red turns off, display indicates `REACHED`.
4. On error, disconnect or timeout: visible `UNKNOWN/FAILED` warning; never claim that a timer alone proves physical position.
5. For STORE: confirmation illumination only when save acknowledgement is actually proven; do not equate sent command with successful save.

**Manufacturer-document distinction:** Datavideo user manual says preset LED illuminates when pressed, and STORE cycle changes LEDs; it does **not** establish that its own LED is a verified physical-arrival sensor. See the official/public instruction manual: https://www.bhphotovideo.com/lit_files/846207.pdf (preset button section and storing presets). The Datavideo specification supports **four preset positions per camera**, not twelve guaranteed positions per camera: https://www.datavideo.com/product/RMC-180%2BMARK%2BII

## One decision still needed — 12-key mapping
The 12 buttons are fixed, but select the **physical grouping and logical mapping** before final CAD:
- **Option A:** Four Datavideo-like camera banks of three keys, assigning three presets to each of **four wired cameras**. This fits within Datavideo's four slots/camera, but CAM5–10 do not have preset keys until expansion.
- **Option B:** Three visually grouped rows/banks of four keys numbered P1–P12 for **the currently selected camera**. More flexible front-panel use across ten camera profiles, but **twelve independently addressable presets on the installed camera/PTZ chain are NOT proven**. Requires technical validation, potential controller-side storage and/or fallback.
No option has been implicitly approved. Trial placeholders may be used in Onshape but should not be frozen for fabrication.

## Friday CAD gate
Screw-removable front panel + removable rear I/O + service access are fixed requirements. Model the chosen illuminated switch/cap and use mechanical clearances; do not cut holes based on the 12×12 mm B3F body. Work from a parametric surface and mark unverified aperture geometry as HOLD. The 350×180 mm R6.2 and 380×210 mm later layout examples are provisional usable panel estimates, **not final overall dimensions**.
Send a preliminary DFM design to Protocase rather than authorizing production when critical cutouts are unknown.

## Source register
Owner Oct 14 decisions; physical reference image; Datavideo manual linked above; Omron B3F sample emails from GMA; WIZnet engineer Theo and Protocase correspondence; R6.2 and R6.3 reviews.
