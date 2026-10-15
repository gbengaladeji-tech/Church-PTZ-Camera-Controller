# R6.5 — Selected-Camera Presets and Illuminated Speed Controls
**Owner update:** 14 October 2026. **Current front-panel decision.** Supersedes R6.4's proposed *per-camera fixed* bank mapping only; **34 button count unchanged**.

## Confirmed behavior
- **10 integrated-illuminated CAM buttons** (only CAM1–4 currently have planned dedicated RS-422 wired interfaces). Illuminate currently selected available CAM; CAM5–10 cannot indicate a working connection until commissioned.
- **12 integrated-illuminated preset buttons**, arranged **four visual groups of three** for the Datavideo aesthetic. Banks are **NOT bound to CAM1–4**; label consecutively P1–P12.
- Selecting CAM 2 and pressing P4 must target **CAM2's preset 4**; CAM3+P4 targets CAM3's position 4. All preset operations are routed through active-camera state.
- **3 illuminated FAST/MIDDLE/SLOW speed buttons**; display exactly one active speed per selected camera profile (pending user preference on global vs per-camera persistence). These are separate from the analog, proportional movement speed defined by the ServoCity 605616 joystick.
- **Illuminated LOCK and AUTO FOCUS mode** also retained. The minimum current illuminated-button target is **27**: 10 CAM + 12 PRESET + 3 speed + LOCK + AF. The remaining **7** of 34 controls may be unlit pending explicit owner decision; white-balance, iris, STORE and others may need illumination and would increase LED/control channels.
- The **25 donated bare B3F-4050 tactiles are valuable only for nonilluminated positions** unless a separate, electrically and mechanically verified cap/LED/light-guide solution is designed. There is no requirement to consume all 25 donated units; do not compromise desired illumination to avoid leaving samples unused. Original GMA September email offered 12 samples; owner counted 25 physically received.
- Fixed **ServoCity 605616** joystick and **NX4024T032_011** display, not assuming touch capability. Enclosure includes screw-removable front panel, rear I/O and bottom service access.

## Important correction: camera/robotic head supports more presets than RMC panel
- **RMC-180 MARK II**: official documentation provides four controller-panel preset shortcuts per camera; manual explicitly says *camera-internal stored settings cannot be accessed by RMC-180 MARK II*. Reference: https://www.datavideo.com/product/RMC-180%2BMARK%2BII and https://www.bhphotovideo.com/lit_files/846207.pdf .
- **PTR-10T MARK II**: Datavideo manufacturer specifications state **50 internal pan/tilt positions**, and PTR-10/T manual says they can be saved using RS-422. Reference: https://www.datavideo.com/ap/product/PTR-10T%2BMARK%2BII and https://device.report/m/3a97df45f8426960832056a276faec83ac8587576f28ca25893c7b7cee7e5ba3
- Therefore **P1–P12 per selected PTR head is plausible** and no longer needs to be artificially reduced to 3 or 4 slots due merely to RMC-180's front-panel limit. However, **exact VISCA RS-422 save/recall format, preset ID base/encoding, available acknowledgements, firmware compatibility, and end-of-travel feedback must still be checked against the connected installed head** before claiming pass.
- PTR stored positions are **pan/tilt presets**; camera lens zoom/focus/iris recall is a separate compatibility matter, not automatically included merely because PTR supports 50 pan/tilt memories.

## Preset LED state (desired, not verified)
1. Idle: white translucent key OFF.
2. Recall initiated: selected Pn RED, display MOVING or REQUESTED.
3. On explicit verified movement completion/arrival: light OFF and display REACHED.
4. Device rejects command, times out, loses RS-422: show ERROR/UNKNOWN and don't falsely claim position reached.
5. If only VISCA ACK or timed expectation exists without position/motion completion feedback, keep feedback labeled as not arrival-confirmed. Confirm command completion semantics on real hardware.

## Physical layout (not cutout-ready)
- Preset visual grouping 4 × 3 (four adjacent blocks each three keys, not labelled by camera).
- Speed FAST/MIDDLE/SLOW group remains together; illuminate only selected mode.
- Manufacturer key top and mounting stack are TBD. Options include Omron B3W-9000-R1C (10×10 mm/red, integrated LED) and more Datavideo-like frosted-white APEM Multimec 5G+1B/2C assemblies with 15.1 mm keycap / 15.5 mm nominal panel cutout. These are **candidates, not purchase approvals**, and must be verified as complete switch+LED+cap+bezel systems. Sources https://www.digikey.ca/en/products/detail/aratas-formerly-omron-components/B3W-9000-R1C/1765388 ; https://www.apem.com/en-us/pcb-switches/mec-tactile-switches-and-accessories/1b-2c-2d/5gsh935611b162d038 .
- 27 Omron B3W units at approx C$4–6 each would cost approximately C$108–162 **before tax/shipping**, and this does not guarantee matching the desired Datavideo appearance. Do not add this hypothetical cost to verified BOM totals.
- R6.2 control-PCB layout, resistor/LED driver count, and previous panel hole locations need redesign once the exact switch family is approved.
- Onshape Friday can lay out keycap envelopes; **do not laser-cut unverified apertures** or manufacture panels before test-fitting one complete illuminated key assembly.

## Current quantity summary
| Control type | Qty | Notes |
|---|---:|---|
| CAM selection | 10 | Must illuminate |
| Preset selection | 12 | Must illuminate |
| FAST/MIDDLE/SLOW | 3 | Must illuminate |
| LOCK | 1 | Must illuminate |
| AUTO FOCUS mode | 1 | Must illuminate |
| Other technical inputs | 7 | Illuminate only after owner prioritizes statuses |
| **All physical buttons** | **34** | **At least 27 illuminated** |
| Planned rotary encoders | 6 | Separate |
| Joystick | 1 | ServoCity 605616 |

Status: **Requirements concept frozen, LED component selection/power/driver circuit and fabricated dimensions still open**.
