# Safety and Deployment Rules

This controller will eventually interact with powered robotic camera equipment used during live church production. Development must therefore be conservative.

## Rules

- Do not climb, open, disconnect, or modify installed church equipment without proper authorization and safe access.
- Do not connect experimental hardware directly to the production system until signal type, pinout, voltage levels, and protocol are verified.
- Treat RS-422/RJ-45 camera-control connections as dedicated control wiring, not ordinary Ethernet.
- Perform initial development with simulation.
- Perform the first real-hardware test with one camera/head only and with production use paused.
- Begin real-hardware tests at low movement speed.
- Keep an immediate stop command available.
- Make movement disabled by default on software startup.
- Stop movement if the input device disconnects or communication becomes invalid.
- Avoid sending unverified commands to live equipment.
- Keep all modifications reversible during testing.

## Deployment goal

The donated/final controller should use secure connectors, strain relief, clear labels, a closed enclosure, replaceable cables, and documented wiring. Prototype breadboards and loose wiring are not suitable for permanent church deployment.
