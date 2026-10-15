# Friday 16 Oct — Enclosure CAD and Protocase Release Gate

## Goal
Complete an editable preliminary enclosure, dimensioned drawings, and a technically truthful handoff. An *unverified* front-panel cutout must not silently become a fabrication drawing.

### 1. The owner's decisions (freeze tonight)
- [x] ServoCity 605616 retained
- [x] CAM 1–10 physical buttons, five by two, CAM5–10 uncommissioned
- [x] 27 buttons total / six encoders / 12 indicators
- [ ] Choose software: Onshape, FreeCAD or Protocase Designer
- [ ] Choose control surface outline and angle (e.g., flat/sloped) and exterior design by owner
- [ ] Place all 27 button centres and six encoder centres, joystick/display centres, plus rear cutouts in one coordinate system

### 2. Photograph/measure the actual parts
- [ ] Nextion **back label/revision** and connector (front and rear photos with ruler)
- [ ] Nextion PCB full outline, four hole centres, screen bezel/front opening
- [ ] Five ordinary donated B3F switches or keycaps close-up from above and side
- [ ] Available caps fitted to B3F and how high they stand from PCB
- [ ] Joystick exact four-hole pattern, vertical envelope, twist/pan/tilt travel and solder tabs (if physically received)
- [ ] One encoder and knob fit coupon with actual panel material/washer/nut (if physically received)
- [ ] Proposed CAM light-guides and LED optics; leave manufacturing openings HOLD without a tested assembly
- [ ] Camera cable connector photos and selected actual power socket model

### 3. CAD reference geometry (NOT aperture release)
- ServoCity flange Ø53.594, total height 85.09, and **Ø100 trial hand-clearance keepout**
- Nextion reference PCB 95×47.6, holes Ø3.20 at 88.60×41.20 — conditional on exact module revision
- Five-by-two CAM centres at pitch22: coordinates relative to CAM block origin (-44,-11),(-22,-11),(0,-11),(22,-11),(44,-11) and same X at Y=+11
- B3F body 12×12; ordinary B32-1310 cap 12×12; **do not cut a 12 mm opening by assumption**
- Six encoder candidate M7×0.75, 6 mm shaft, trial knob Ø20
- W55 PCB 80×21 but outer components overhang to ≈85.35 length
- R6.2 350×180 denotes **flat usable planning area**, not exterior enclosure dimensions or accepted minimum

### 4. Protocase submission package
- [ ] Editable CAD source (+ revision label)
- [ ] Correctly oriented STEP or SolidWorks Pack and Go
- [ ] Dimensioned PDF of exterior and all *approved* cutouts
- [ ] Material and thickness (candidate: stock 5052-H32 1.63 mm)
- [ ] Finish (including coating thickness on cutout clearance)
- [ ] Quantity: 1; labels and legends
- [ ] Assembly strategy (removable panel? standoffs/brackets? access to wiring and main board)
- [ ] Tolerance stack on coated caps and threaded encoders
- [ ] Critical unknowns explicitly annotated on separate HOLD layer/notes
- [ ] Request engineering DFM check and confirm $500 CAD sponsorship applied to quote; timing for November 6 is **not guaranteed**

### Decision at end of Friday
**Release for manufacture:** all openings, mounts and bend geometry verified, quotes/DFM accepted, and owner signs off.

**Otherwise:** send *preliminary for feedback*, request missing part/sample/fit checks, and agree a revised timeline. Do not order production from a provisional model.

**Deferred from Friday:** fully functional KiCad design, firmware, supervised real-camera test and commissioning. These affect system safety/function, not the initial shape sketch.
