"""Transport abstractions for the PTZ controller.

SimulationTransport is the only enabled transport at the start of the project.
A real RS-422 transport will be added only after protocol bytes, pinout, and
hardware configuration are verified.
"""

from abc import ABC, abstractmethod
from .commands import PTZCommand


class Transport(ABC):
    @abstractmethod
    def send(self, command: PTZCommand) -> None:
        raise NotImplementedError


class SimulationTransport(Transport):
    def send(self, command: PTZCommand) -> None:
        preset = f", preset={command.preset}" if command.preset else ""
        print(
            f"[SIM] camera={command.camera}, "
            f"action={command.action.value}, speed={command.speed}{preset}"
        )
