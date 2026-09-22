# Safety and Deployment Rules

This controller will eventually interact with powered robotic camera equipment used during live church production. Development must therefore be conservative.

## Rules

- Do not climb, open, disconnect, or modify installed church equipment without proper authorization and safe access.
- Do not connect experimental hardware directly to the production system until signal type, pinout, voltage levels, and protocol are verified.
- Treat the four RS-422/8P8C camera-control connections as dedicated control wiring, not ordinary Ethernet.
- Keep the real W5500 Ethernet port physically and logically distinct from RS-422 camera ports.
- Clearly label rear-panel RS-422 camera-control ports so they cannot reasonably be mistaken for LAN connections.
- Perform initial protocol development in simulation/reference tests.
- Prove one RS-422 channel before duplicating the circuit across all four camera ports.
- Perform the first real-hardware test with one camera/head only and with production use paused.
- Begin real-hardware tests at low movement speed.
- Keep an immediate STOP / movement-disable function available.
- Make movement disabled by default on startup and after profile changes where practical.
- Stop movement if the input device disconnects or communication becomes invalid.
- Selecting an unassigned CAM 5-10 profile must not transmit arbitrary camera commands.
- Avoid sending unverified commands to live equipment.
- Keep all modifications reversible during testing.
- Do not claim DVIP/IP compatibility until the specific network protocol and target hardware have been verified.

## Deployment goal

The donated/final controller should use secure connectors, strain relief, clear labels, a closed enclosure, replaceable cables, serviceable internal wiring, and documented pinouts.

Prototype breadboards and loose wiring are not suitable for permanent church deployment.