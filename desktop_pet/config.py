"""Configuration and constants for Desktop Pet."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple

BASE_SIZE = 64          # Logical sprite size in pixels (before scaling)
ANIM_FRAMES = 20        # Length of one animation cycle, in ticks
ANIM_HALF = ANIM_FRAMES // 2

RGB = Tuple[int, int, int]


class PetState(Enum):
    WALK = auto()
    IDLE = auto()
    SLEEP = auto()


@dataclass(frozen=True)
class Palette:
    body: RGB = (35, 39, 46)
    outline: RGB = (0, 255, 170)
    sleeping_eye: RGB = (120, 120, 120)


@dataclass(frozen=True)
class PetConfig:
    scale: float = 1.0                 # Size multiplier
    speed: float = 2.0                 # Pixels per tick while walking
    fps: int = 30                      # Ticks per second
    margin: int = 10                   # Gap to screen edges, in pixels
    state_duration: Tuple[int, int] = (90, 250)   # Ticks before re-rolling behaviour
    state_weights: dict = field(
        default_factory=lambda: {
            PetState.WALK: 0.60,
            PetState.IDLE: 0.25,
            PetState.SLEEP: 0.15,
        }
    )
    palette: Palette = field(default_factory=Palette)
