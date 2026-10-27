# Hardware status, R6.8

27 October 2026. [Current BOM](r68/BOM_and_Acquisition.csv) separates owned, approved and candidate parts. APEM keys, joystick, encoders and protection circuits are not falsely marked received or released. The approved W55 sample has no dispatch/receipt proof in the inspected thread.

[Electrical design](r68/Electrical_Design.md) contains the proposed topology. [Pin map](r68/Pin_Map.csv), [48 input slots](r68/Input_Map.csv) and [32 output slots](r68/LED_Map.csv) define the development harness. Six HC165 permit symmetrical local input banks;34 slots are used. Four HC595 feed transistor sinks;27 output slots are assigned. This recommendation does not establish final board outlines, fit or fabrication cost.

A new native KiCad design, selected exact protection/connector parts and clean ERC/DRC are still required. No production Gerbers are supplied. The historical D1 findings remain unresolved.
