# Acceptance record

Record date, actual hardware/firmware revision, operator, test setup, expected result, actual result and pass/fail. An unrun test stays NOT RUN.

| ID | Test and pass condition | Current result |
|---|---|---|
|HOST01|Existing 4 command unit tests pass|PASS on host, 27 Oct 2026|
|HOST02|13 new R6.8 safety/map tests pass|PASS on host, 27 Oct 2026|
|HOST03|Existing legacy controller assertions pass|PASS on host; legacy addressing is not new profile|
|HOST04|New Python files parse without syntax errors|Run result in Test_Results.txt|
|MECH01|Actual Onshape centres recorded for 33 controls|NOT RUN; document unavailable|
|MECH02|One complete key works in final finish/thickness coupon with full travel|NOT RUN|
|MECH03|Joystick/encoder/screen stack and mated plug fit|NOT RUN|
|MECH04|Each panel removes with service plugs accessible and no interference|NOT RUN|
|POWER01|No shorts; correct jack polarity; protected rail within part limits|NOT RUN|
|POWER02|USB/external service cases produce no backfeed or I/O injection|NOT RUN|
|POWER03|Measured steady, inrush and thermal budget within ratings with margin|NOT RUN|
|INPUT01|Walking contact test covers 48 slots; spares defined; simultaneous presses correct|NOT RUN|
|INPUT02|Encoders count bidirectionally without missed edges under maximum bus load|NOT RUN|
|INPUT03|ADC calibration and all wire-break cases fail safely|NOT RUN; range guard alone insufficient|
|LED01|Walking 27 lamps maps correctly; spares off; safe current and brightness|NOT RUN|
|BOOT01|Driver EN remains LOW through power-on, flash, reset and watchdog until intentional arming|NOT RUN|
|UART01|38400 8N1 observed; each PIO channel passes loopback/error stress at actual baud|NOT RUN|
|UART02|Reply parser handles fragments, invalid frames, errors, sockets and completion without blocking|NOT IMPLEMENTED|
|CAM01|One installed head model, firmware, DIP, address and cable verified|NOT RUN|
|CAM02|Minimum-speed pan/tilt/zoom/focus and three STOP domains validated|NOT RUN|
|CAM03|CAM change stops old head before new motion; CAM5-10 never transmit|NOT RUN|
|CAM04|Serial loss, joystick break, cable pull, power cut/watchdog and recovery behaviour documented|NOT RUN|
|CAM05|12-preset mapping and STORE confirmation proved; ACK never means reached|NOT RUN|
|CAM06|Unsupported functions display Unavailable and never claim state|NOT RUN|
|CAM07|All four heads pass sequential and simultaneous load tests|NOT RUN|
|IP01|Ethernet qualified separately without control of the same head by IP and serial|NOT IMPLEMENTED; CAM5-10 disabled|
|FAB01|Manufacturer accepts revision, fit, finish, hardware and delivered owner balance|NOT RUN|
|PCB01|Native ERC/DRC reports and review close all fatal findings|NOT RUN|

Bench progression: inspect unpowered, prove power rails, one input/LED, joystick/screen, differential loopback, all serial channels, one supervised head, then four. Keep existing controller available and avoid active services.

Operational faults must latch disarmed. Input timeout target100ms and neutral dwell500ms are reference design choices, not proof of remote stopping. STOP packets have priority and must finish transmission before disabling the driver. A reset or power cut cannot guarantee STOP delivery; local inhibit and remote rest are separate facts. No production deploy until the observed behaviour is acceptable to the church technician.
