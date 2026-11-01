# System architecture

This filename is retained for links from the original V1 documentation. The
current detailed design is in [SOFTWARE_ARCHITECTURE.md](SOFTWARE_ARCHITECTURE.md).

The current target is a standalone W55RP20-based console. Keyboard, Xbox, and
Arduino-to-Python paths remain useful simulations but are no longer the final
deployment architecture.

```text
physical controls -> W55RP20 firmware -> verified full-duplex RS-422 -> PTR head
                                  +----> Nextion status
                                  +----> separate LED indicators
```

The ten logical camera keys do not imply ten physical ports. Routing remains a
configuration boundary, with four wired routes enabled and six disabled by
default.
