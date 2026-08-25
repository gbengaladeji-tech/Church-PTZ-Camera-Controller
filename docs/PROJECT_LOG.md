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

## 2026-08-25 — Python stopped feeling random and started becoming the controller

**Phase:** Python/VISCA learning → beginning actual controller software

### What I did

Today I finished the little Python pieces I needed before starting the real controller software.

I fixed the error where an invalid speed made `build_packet()` return `None`, but then the program still tried to loop through the result and crashed. I changed the logic so the program checks if the result is `None` first. If it is, it prints that the packet was rejected. If it is not `None`, then it is safe to format the packet.

I also made `get_camera_header(camera)`. Instead of me always manually remembering that Camera 1 is `0x81`, Camera 2 is `0x82`, etc, I figured out that I can use `0x80 + camera`. So if the selected camera is 3, Python can calculate `0x83` for me.

Then I made `get_direction(movement)`. This was important because I do not want the final controller thinking in raw numbers all the time. I want the software to be able to understand normal things like `left`, `right`, `up`, `down`, `stop`, and the diagonal movements, then translate those into the correct VISCA horizontal and vertical values.

I also started moving the functions I actually understand into a new `controller_v1.py` file locally so the project can move out of the learning/practice stage and into the actual controller software.

### What I learned from `check_speed()`

This helped me understand validation more. A program should not just accept every number and hope it works. It should check if the input makes sense before doing anything with it.

For the pan/tilt speed I am currently using the VISCA range `1–18`. If the speed is outside that range, the program rejects it instead of building a normal packet.

### What I learned from the `None` error

This was probably one of the most useful bugs so far because I finally understood what `None` actually means in practice.

When `build_packet()` returns `None`, there is literally no packet there to loop through. My old code still tried to do `for value in result`, which caused the `NoneType is not iterable` error.

Now I understand the logic as:

`result is None` → there is no packet → reject it

`result is not None` → there is a packet → it is safe to format/use it

### What I learned from `get_camera_header()`

Before this, I was manually putting values like `0x81`, `0x82`, and `0x83` into the packet.

Now I understand that the software can keep something simple like `camera = 3`, and another function can translate that into the VISCA header.

That showed me why functions are useful in a real program. The rest of the software does not need to care about how the header is calculated. It can just ask the function for it.

### What I learned from `get_direction()`

This taught me how I can translate something a human understands into something the camera protocol understands.

For example:

`left` → `0x01, 0x03`

`up_right` → `0x02, 0x01`

`stop` → `0x03, 0x03`

I also learned that one function can return two values at the same time. That is useful here because VISCA pan/tilt movement needs a horizontal value and a vertical value.

### What I learned about variables being replaced

When I did this several times:

`Horizontal, Vertical = get_direction(...)`

the newest result replaced the old values stored in `Horizontal` and `Vertical`.

That helped me understand that a variable is basically holding the current value. If I assign something new to it, the old value is replaced.

This will matter later because the selected camera, movement, and speed will all change while the operator is using the controller.

### How the software pieces work together now

The way I understand it now is:

`camera number` → `get_camera_header()` → VISCA camera header

`movement word` → `get_direction()` → horizontal + vertical VISCA values

`speed` → `check_speed()` → accepted or rejected

all of those values → `build_packet()` → final VISCA pan/tilt packet

So instead of me manually creating something like:

`82 01 06 01 05 05 01 03 FF`

I am working toward being able to give the controller normal information such as:

- Camera 2
- Move left
- Medium speed

and let my software translate that into the packet.

### Biggest thing I learned today

This was the point where Python stopped feeling like a bunch of random things like functions, `if` statements, `return`, and variables.

I can finally see how those basic things become the actual controller.

Each function has one job, and then the jobs connect together.

### Next

Next I want to add the human-friendly speed modes:

- slow
- medium
- fast

After that I want to combine camera selection + movement + speed into one complete controller command and then make a WASD keyboard simulation so I can actually control the software before I have physical hardware connected.

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
