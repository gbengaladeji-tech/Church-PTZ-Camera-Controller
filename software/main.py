"""Keyboard-driven PTZ controller prototype.

This does not communicate with church equipment. It only exercises the planned
control flow through SimulationTransport.
"""

from ptz import Action, PTZCommand, SimulationTransport


KEYS = {
    "a": Action.PAN_LEFT,
    "d": Action.PAN_RIGHT,
    "w": Action.TILT_UP,
    "s": Action.TILT_DOWN,
    "x": Action.STOP,
    "+": Action.ZOOM_IN,
    "-": Action.ZOOM_OUT,
}


def main() -> None:
    transport = SimulationTransport()
    camera = 1
    speed = 25

    print("Church PTZ Controller — simulation")
    print("1-4 camera | WASD move | X stop | +/- zoom | Q quit")

    while True:
        raw = input(f"CAM {camera} @ {speed}% > ").strip().lower()

        if raw == "q":
            transport.send(PTZCommand(camera=camera, action=Action.STOP, speed=speed))
            break

        if raw in {"1", "2", "3", "4"}:
            camera = int(raw)
            print(f"Selected Camera {camera}")
            continue

        if raw.startswith("speed "):
            try:
                speed = int(raw.split(maxsplit=1)[1])
                if not 1 <= speed <= 100:
                    raise ValueError
                print(f"Speed set to {speed}%")
            except ValueError:
                print("Speed must be an integer from 1 to 100")
            continue

        action = KEYS.get(raw)
        if action is None:
            print("Unknown command")
            continue

        transport.send(PTZCommand(camera=camera, action=action, speed=speed))


if __name__ == "__main__":
    main()
