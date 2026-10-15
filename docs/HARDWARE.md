# Hardware and procurement status

Use the [current canonical BOM](engineering/VERIFIED_MASTER_BOM.xlsx) and [component/mount schedule](engineering/ONSHAPE_CAD_MASTER_DIMENSIONS.xlsx). The96 legacy records are mapped once in the BOM; archived prices do not feed current totals.

| Assembly | Current basis | Status |
|---|---|---|
| Joystick | ServoCity605616 | Fixed selection; not evidenced owned. Both pitches/opening/sweep still need fit verification. |
| Display | NextionNX4024T032_011 | Owned; actual suffix/window and cable stack unverified; no touch dependency. |
| Illuminated keys | APEM3FTH9871KC11162K09, quantity27 | Catalogued candidate. Quote/MOQ/lead time, exact stack and coupon open. Request already sent. |
| Unlit keys | B3F-4050 quantity7, B32-1310 caps quantity7 |25 bare switches owned per owner;18 remain unused. Caps not owned. |
| Encoders/knobs | PEC11R-4220F-N0024 / Adafruit5527, quantity6 | Candidate fit set; encoder has no push switch, nut/washer included; knob height conflict open. |
| Controller | W55RP20-EVB-PICO sample | Approved, confirmation sent, no shipment/receipt evidence.19 usable external GPIO. |
| Digital interface |6 HC165;4 HC595;27 sink stages |46 inputs/27 LEDs. Specification only; previous12-LED PCB obsolete. |
| RS-422 | AM26LV31EIDR +AM26LV32EIDR, four serial jacks | Conditional candidates. Termination/bias/protection/grounding and hardware tests open. |
| Power |5V/3A GST18U05-P1J candidate | Fuse, input jack, USB arbitration, inrush and thermal design incomplete. |
| Enclosure | Proposed stock5052-H32,1.6256mm |C$500 Protocase support including shipping; final quote/tax/delivery open. |

Current-priced mechanical/power subsetC$120.27 before HST/freight. Full remaining costUNKNOWN. No orders or new supplier messages were sent. The baseline's all25-switch installation, B3W AF/LOCK and separate green CAM LEDs are superseded.

Never connect the four RS-422 sockets to Ethernet/PoE. First validate one channel with agreed spare camera presets, then expand tofour. Retain RMC fallback without paralleling its line drivers. [Full decisions and limitations](engineering/FINAL_PROJECT_DECISIONS.md).
