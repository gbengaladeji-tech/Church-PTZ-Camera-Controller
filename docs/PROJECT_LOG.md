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

## 2026-08-25 — Keyboard test harness + controller state milestone

**Phase:** Software simulation / controller logic validation

### What I built

I connected the little functions together so the program can now take normal controller-style choices and turn them into a full VISCA packet automatically.

The program now keeps track of a selected camera and selected speed, accepts a movement command, translates everything, builds the packet, and prints it in the same hexadecimal style as the manual.

I also added a simple keyboard test harness:

- `1–4` changes the selected camera
- `5` = slow
- `6` = medium
- `7` = fast
- `W/A/S/D` = movement
- `X` = stop
- invalid keys are rejected instead of reusing the previous movement

### Important design decision — the keyboard is NOT the final controller

The keyboard controls are only here for testing the software while I do not have the physical control hardware connected yet.

I want to keep this keyboard mode in the project because it is useful for debugging and testing packets, but the actual goal is still the physical church controller I am building with a joystick, camera-selection controls, speed controls, zoom, presets, and the rest of the operator interface.

The useful part is that the VISCA/controller logic should not care whether the command originally came from a keyboard or from the physical controller. Later the Arduino/ESP32 input layer should provide the same kind of normal actions to the controller logic.

So the keyboard is basically a temporary/test input layer, not the main product.

### What I learned from calling functions

I made the mistake of writing:

`result = build_packet`

and Python printed something like `<function build_packet at ...>`.

That taught me the difference between referring to a function and actually calling it.

`build_packet` = the function itself.

`build_packet(...)` = run the function with inputs.

I also finally understood exactly where the packet values come from. The values are not magically appearing inside `build_packet()`. They are returned from the other functions, saved into variables, then passed into the packet builder.

### What I learned about controller state

This made variables make way more sense.

`selected_camera` can stay as Camera 3 until I press another camera button.

`speed_mode` can stay as slow until I change it.

Movement is different because it changes every time I give a movement command.

This is the first time I really understood the idea of the program having a current state instead of recalculating/randomly setting everything every time.

Also only one camera is selected because `selected_camera` is one variable. If it changes from `1` to `3`, Camera 1 is not still selected in software. The old value was replaced.

### What I learned from `while True`

Before this, the program ran one command and ended.

I learned that `while True:` can keep the test controller alive so it keeps asking for commands.

The important part was indentation. At first I put only the input inside the loop, which made everything underneath grey/unreachable because Python saw an infinite loop before the rest of the controller code.

That helped me understand that indentation is not just formatting in Python. It decides what code actually belongs to the loop.

### What I learned from `continue`

`continue` means stop the current trip through the loop and go back to the top.

This ended up being useful in two places:

- after changing camera/speed, because selecting something should not also create a movement packet
- after an invalid key, because an invalid input should not reach the packet builder

### Bug I found with invalid keys

Originally if I pressed `D`, movement became `right`.

Then if I pressed a random key like `F`, none of the movement conditions changed the variable, so `movement` was STILL `right` and the program built another right packet.

That is not something I would want on the actual controller.

I added an `else` with `continue`, so invalid inputs now stop before a packet is built.

This was a useful lesson in why input validation matters even if the packet builder itself is correct.

### Another bug I caused — too many `input()` calls

At one point I had a separate `key = input()` before Camera 1, another before Camera 2, another before Camera 3, etc.

That meant one keypress could get consumed by one check and then the program immediately asked for another key before reaching the rest of the logic.

I learned that I only need ONE input at the top of each loop, then all the camera/speed/movement checks inspect that same value.

### Speed modes

I added a translation function for the temporary speed modes:

- slow → `0x04`
- medium → `0x09`
- fast → `0x12`

These are starting simulation values, not final tuned physical-controller speeds.

### Test evidence

I tested:

Camera 3 + slow + up:

`83 01 06 01 04 04 03 01 FF`

Camera 4 + fast + right:

`84 01 06 01 12 12 02 03 FF`

I also tested all four basic movement directions, stop, camera selection, speed selection, and random invalid keys.

### Biggest thing I learned from this milestone

The part that clicked for me is that the controller can be separated into layers.

The keyboard is just telling the software what I want during testing. The important controller logic underneath is translating that request into the correct VISCA command.

Later I should be able to replace the keyboard input with the physical joystick/buttons without throwing away the VISCA work I already made.

That is much closer to how I want the final controller to be designed.

### Next milestone

Keep the keyboard test harness in the code for simulation/debugging, but do not spend the project turning it into a keyboard controller.

The main direction stays the physical controller. The next software work should expand the real command layer and prepare clean inputs that the future Arduino/ESP32 + joystick/buttons can use.

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
