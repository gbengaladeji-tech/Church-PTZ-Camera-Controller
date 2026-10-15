> **SUPERSEDED on 14 October (R6.4):** The owner reduced illuminated presets from 16 to **12**, giving **34 total pushbuttons** (10 CAM + 12 PRESET + 12 technical), not 38. See [the current R6.4 controls document](CONTROL_REVISION_2026-10-14_R6_4_PRESETS.md). The text below remains historical.\n\n# Control and Illumination Decision — 14 October 2026 (supersedes 27-key baseline)
**Status:** new control layout requirement; neither the R6.2 control-key BOM nor control PCBs are frozen.

## Confirmed owner intent
- Reference front-panel grouping: Datavideo RMC-180 MARK II, but ten physical CAM selectors instead of four.
- Onshape CAD: professionally sloped, **screw-removable front control panel**, independently removable rear I/O panel, and service access. These are original project constraints, not newly proposed.
- ServoCity 605616 joystick stays fixed.
- CAM1–10 buttons are **true illuminated pushbutton assemblies**, not donated unlit tactiles with separate exposed light dots. Camera5–10 remain disabled/uncommissioned until proven future connection support exists.
- The received switches are **25 bare Omron B3F-4050 tactile units (no B32 key tops/caps, no LEDs)**. GMA's original September offer described twelve samples, while the owner counted twenty-five physical units. The physical count controls inventory, but model markings must still be checked.
- Owner display back label: `NX4024T032_011`. Published family includes non-touch `...011N` and resistive-touch `...011R`. Owner has not observed functioning touch. Design menu navigation by physical encoders and buttons; do not depend on touch input.
- At least the LOCK and AUTO FOCUS status buttons are intended to light; the previous supplier requests for **two** separate illuminated control switches do not cover the **ten additional CAM illuminated switches**.

## Recalculated Datavideo-equivalent physical button count
| Group | Original RMC | New controller |
|---|---:|---:|
| Camera selection | 4 | **10** |
| Preset keys (4 banks of 4) | 16 | **16** |
| STORE | 1 | 1 |
| FAST/MIDDLE/SLOW | 3 | 3 |
| LOCK | 1 | 1 |
| Focus/manual | 1 | 1 |
| CAM OSD | 1 | 1 |
| ONE PUSH white balance | 1 | 1 |
| MWB | 1 | 1 |
| ATW | 1 | 1 |
| IRIS | 1 | 1 |
| SHUTTER | 1 | 1 |
| **Total** | **32** | **38** |

These are *reference-style functions* and front-panel positions, not assertions that all commands are available on installed Panasonic / PTR camera profile. No oversized STOP or extra zoom buttons are to be added. The owner previously specified AUTO FOCUS directly beneath FOCUS knob; integrate this in the confirmed focus-mode controls without making a redundant duplicate before owner approval.

**R6.2's previous 27-button and 12-indicator BOM targets are obsolete for this new owner request.** R6.2's six encoders are still the existing candidate arrangement; do not automatically add an encoder unless owner explicitly confirms.

## Illumination requirements and cost gate
- **Must illuminate in button:** 10 CAM selectors (10 separate illuminated assemblies).
- **Must provide clear lit state:** LOCK, AUTO FOCUS/manual status; check whether existing candidate B3W-9000-G1C is green rather than red.
- **Photo-style lit behavior, exact technology to approve before buying:** sixteen presets, FAST/MIDDLE/SLOW, white-balance mode, iris/shutter, STORE.
- Backlit controls require *independent LED drive current and shift-register outputs*; no longer assume 12 LED channels in the current PCB architecture.
- Donated B3F mechanical switches can be reused for nonilluminated controls; they require appropriately fitted *separately purchased key tops* and support PCB datum.
- If every backlit function uses an **integrated** backlit switch, most received B3Fs may go unused. Cost this separately before a commitment. Do not assume all 25 must be installed.
- Consider red LED **Omron B3W-9000-R1C** as one candidate for uniformly lit 10mm key; R1C is red whereas **B3W-9000-G1C is green**, per Omron manufacturer table. Verify suitable procurement, PCB footprint, illumination, and front panel aperture before design lock.
- Accurate red/white state representation may require dual-color LEDs or independent feedback; a red-only LED cannot light white. No visual state feedback implies no camera acknowledgement.

## CAD release HOLD
- Change base Onshape layout before proceeding: **38 buttons, not 27; ten CAM buttons; sixteen presets; removable front/rear plates**. Do not make 27 committed sheet-metal apertures.
- The chosen illuminated key type determines each CAM aperture/support. CAM 22mm pitch is provisional.
- Nextion 95×47.6 board is not a display-window cutout.
- Enclosure trial envelope must be repacked for 38 keys; R6.2 350×180 and later 380×210 were *reference panel sizes*, not confirmed manufacturing dimensions.
- Final manufacturing cutouts and pressed/tapped hardware mounts cannot be certified without fit-check samples or qualified manufacturer drawings.
- Protocase Friday submission can be a **preliminary DFM package** if critical cuts remain HOLD, but must not be labelled production-ready.

## Source references
- Omron B3W-9 (illuminated): https://components.omron.com/sites/default/files/datasheet_pdf/A167-E1.pdf
- Omron B32 key tops: https://components.omron.com/sites/default/files/datasheet_pdf/A077-E1.pdf
- Nextion 011N / 011R family: https://nextion.ca/datasheets/nx4024t032_011/
- Datavideo manual: https://www.bhphotovideo.com/lit_files/846207.pdf
- Gmail: supplier B3F sample conversation September 29–October 5; illuminated switches requests October 12.
- Companion workbook: `Church_PTZ_R6_3_Control_Illumination_and_CAD_Delta.xlsx` in user handoff (not yet committed to git).
