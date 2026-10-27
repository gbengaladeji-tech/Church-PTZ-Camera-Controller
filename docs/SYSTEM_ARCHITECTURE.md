# Proposed architecture, R6.8

![Wiring topology](r68/Complete_Block_Diagram.svg)

W55RP20 reads buttons/encoders through six3.3V input shift registers, joystick voltages through three ADC pins, and the display through a safely level-converted UART. Four output shift registers drive27 separate LED sinks. UART0 and three proposed PIO pairs serve four independent full-duplex RS-422 ports. UART1 serves Nextion. GP15 controls only driver enable; the input/LED clock is shared to fit19 available pins.

Certified external5V power, protected distribution, separate auxiliary3.3V and verified USB/backfeed behaviour are required. The diagram is a design proposal. See [detailed limits](r68/Electrical_Design.md). Ethernet/IP remains a future qualification task; it is not enabled for CAM5-10.
