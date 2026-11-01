# W55RP20 firmware

This directory contains the new controller core. It is C++17 so the safety,
input-processing, routing, display, and VISCA logic can run both on a computer
and on the W55RP20's RP2040 core.

Run the host tests with:

```bash
make -C firmware test
```

`CMakeLists.txt` is the production Pico SDK entry point. It deliberately does
not assign GPIO or enable physical transmission yet: the five simultaneous
serial links, RS-422 pinout, transceiver enables, and Nextion voltage interface
are unresolved hardware release gates. See `docs/WIRING.md`.

The host test build requires only a C++17 compiler. The RP2040 build additionally
requires the Raspberry Pi Pico SDK, CMake, and the Arm embedded compiler.
