# Engineering Project Log

This file records the engineering process: observations, assumptions, decisions, experiments, failures, test results, revisions, and next steps.

---

## 2026-08-23 — Project Initiated

**Timestamp:** 2026-08-23 02:55 UTC  
**Phase:** Planning / existing-system investigation

### Work completed

- Created the public GitHub repository for the project.
- Documented the purpose and initial V1 scope.
- Photographed and investigated the existing church camera system.
- Identified the Datavideo RMC-180 MARK II as the current operator controller.
- Identified Datavideo PTR-10/T MARK II robotic pan/tilt hardware.
- Identified Panasonic professional 4K camcorders mounted to the robotic heads.
- Identified RS-422 and Sony VISCA as key technologies to investigate.
- Decided to communicate with the existing robotic heads rather than attempt to drive their motors directly.
- Decided that the first prototype will be software/simulation-first before any connection to church production equipment.

### Initial design direction

The controller should prioritize:

1. Physical joystick pan/tilt control.
2. Physical zoom control.
3. Four clearly indicated camera-selection buttons.
4. Named church shot presets.
5. Adjustable movement speed.
6. Clear operator feedback.
7. Movement enable/disable and stop controls.
8. Modular hardware and software.
9. A low-cost prototype before a polished donated unit.

### Current engineering question

What is the safest, simplest, and most reliable method for generating documented VISCA commands in software and later transmitting them through an appropriate RS-422 interface to a PTR-10/T MARK II?

### Next milestone

Build a software-only command prototype that can:

- select a camera,
- accept pan/tilt/stop input,
- generate a command object/packet representation,
- print the result through a simulated transport layer,
- and be tested without moving real equipment.

---

## Log entry template

### YYYY-MM-DD — Title

**Timestamp:**  
**Phase:**

### Goal

### Work completed

### What worked

### What failed / unexpected behavior

### Evidence / measurements

### Design decision

### What I learned

### Next milestone
