"""High-level PTZ command definitions.

This module intentionally starts protocol-agnostic. Exact VISCA byte packets should
only be added after they are checked against the official Datavideo documentation.
"""

from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    STOP = "stop"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    PRESET = "preset"


@dataclass(frozen=True)
class PTZCommand:
    camera: int
    action: Action
    speed: int = 1
    preset: str | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.camera <= 4:
            raise ValueError("camera must be between 1 and 4")
        if not 1 <= self.speed <= 100:
            raise ValueError("speed must be between 1 and 100")
        if self.action is Action.PRESET and not self.preset:
            raise ValueError("preset commands require a preset name")
