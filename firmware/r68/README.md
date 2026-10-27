# R6.8 disconnected bench development

`diagnostic.py` reads a proposed48-bit input chain and three ADC axes, writes LED words only when explicitly called, and holds GP15 driver enable LOW. Use only after electrical review with no camera cables. Run manually, not as automatic main.py. `pins.py` defines the proposed harness.

`pio_uart.py` is experimental38400 8N1 loopback transport. Allocate TX/RX state machines0/1 onGP2/3,2/3 onGP6/7 and4/5 onGP8/9. UART0GP0/1 is the first camera pair and UART1GP4/5 the screen. No framing-error reporting or production scheduling/parser is provided. Validate exact MicroPython build, baud and concurrent loading on actual W55 hardware. Host compileall is not an embedded compile or board test.

See docs/r68 for the electrical/acceptance gates. A complete production controller firmware binary has not been produced.
