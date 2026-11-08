# PTZ R9 firmware candidate

The startup entry point leaves the RS-422 driver disabled. The target implements input scanning, independent lamps, encoders, ADC diagnostics and explicitly gated isolated loopback. Pan/tilt/zoom, focus, iris, presets and STOP are logical intents on this revision. Live Datavideo camera packet output is held pending an exact protocol and on-target checks. Ethernet functions and CAM5–CAM10 are unavailable.

Use the [WIZnet board-specific MicroPython builds](https://github.com/Wiznet/RP2040-HAT-MicroPython/releases). Check that the downloaded asset explicitly names W55RP20-EVB-PICO. Use the four `.py` runtime files by default. The test compilation used MicroPython cross-compiler 1.29, bytecode ABI 6.3. Compilation checks source syntax and bytecode generation. The UF2, assembler execution, UART sampling, PIO FIFO, concurrent traffic and Ethernet coexistence need the physical board.

| Resource | Assignment |
|---|---|
| UART0 GP0/GP1 | CAM1 TX/RX |
| UART1 GP4/GP5 | Nextion at diagnostic setting 9600 |
| PIO SM0/1 GP2/GP3 | CAM2 TX/RX |
| PIO SM2/3 GP6/GP7 | CAM3 TX/RX |
| PIO SM4/5 GP8/GP9 | CAM4 TX/RX |
| GP10–15 | CLOCK, LOAD_N, INPUT_DATA, LED_DATA, LED_LATCH, RS_ENABLE |
| GP26/27/28 | Pan, tilt, twist analog inputs |

Run host tests with `python3 -m unittest -v test_core` in this directory. Run the target only with its independent camera and LAN cables disconnected. With an isolated dummy wired and checked, `target.loopback(1, "ISOLATED_DUMMY_ONLY")` expects one local echo on port 1. The `38400` default is for the dummy, and requires matching settings at both ends. Run `target.diagnostics(30)` for contacts and raw ADC. For calibrated local intent supply three measured normalized (minimum, neutral, maximum) tuples as `calibration=`. Test data are illustrative. Repeated use of USB REPL Ctrl-D resets the MCU and the target; power cycling AUX separately is required to test hardware LED power-on blanking.
