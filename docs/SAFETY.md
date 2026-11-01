# Safety and deployment rules

- Keep simulation and loopback as the default development modes.
- Do not connect an unverified 8P8C cable or transceiver to church equipment.
- Confirm exact pinout, polarity, voltage, termination, bias, reference, and
  protocol with power removed and an independently reviewed diagram.
- First motion testing uses one authorized non-production head, minimum speed,
  an observer, clear mechanical area, immediate fallback, and the original
  controller available.
- Startup requires neutral. Invalid/stale input, route changes, shutdown, and
  reply timeout attempt stop.
- A software stop attempt is not a guaranteed remote stop. Loss of power or a
  broken cable may leave the remote system in its last commanded state.
- Use certified low-voltage power, current limiting during bench work, fusing,
  reverse/backfeed protection, strain relief, closed insulation, and documented
  chassis/ground strategy.
- Never use a breadboard, loose wiring, or an unreviewed commissioning image in
  regular church production.
- Preserve logs and stop testing at the first unexplained movement, hot part,
  wrong voltage, communication error, or damaged data.
