"""The pet window: behaviour, movement and the main loop."""

import random
from typing import Optional

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget

from .config import ANIM_FRAMES, BASE_SIZE, PetConfig, PetState
from .renderer import draw_pet


class DesktopPet(QWidget):
    """A frameless, transparent, click-through window that walks along the screen bottom."""

    def __init__(self, config: Optional[PetConfig] = None) -> None:
        super().__init__()
        self._config = config or PetConfig()
        self._size = max(16, round(BASE_SIZE * self._config.scale))

        self._state = PetState.WALK
        self._direction = 1  # 1 = right, -1 = left
        self._frame = 0
        self._state_ticks = 0
        self._state_duration = self._roll_duration()

        self._setup_window()
        self._setup_bounds()

        self._x = random.uniform(self._min_x, self._max_x)
        self.move(round(self._x), self._y)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(max(1, 1000 // self._config.fps))

    # ------------------------------------------------------------------ setup

    def _setup_window(self) -> None:
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowTransparentForInput  # Clicks pass through to windows below
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)
        self.resize(self._size, self._size)

    def _setup_bounds(self) -> None:
        """Compute the walkable area from the primary screen's usable geometry."""
        screen = QApplication.primaryScreen().availableGeometry()
        margin = self._config.margin
        self._min_x = screen.left() + margin
        self._max_x = max(self._min_x, screen.left() + screen.width() - self._size - margin)
        self._y = screen.top() + screen.height() - self._size - margin

    # ---------------------------------------------------------------- control

    @property
    def paused(self) -> bool:
        return not self._timer.isActive()

    def set_paused(self, paused: bool) -> None:
        if paused:
            self._timer.stop()
        elif not self._timer.isActive():
            self._timer.start(max(1, 1000 // self._config.fps))

    # --------------------------------------------------------------- behaviour

    def _roll_duration(self) -> int:
        return random.randint(*self._config.state_duration)

    def _pick_next_state(self) -> None:
        states = list(self._config.state_weights)
        weights = list(self._config.state_weights.values())
        self._state = random.choices(states, weights=weights)[0]
        if self._state is PetState.WALK:
            self._direction = random.choice((-1, 1))

    def _tick(self) -> None:
        self._frame = (self._frame + 1) % ANIM_FRAMES
        self._state_ticks += 1

        if self._state_ticks >= self._state_duration:
            self._state_ticks = 0
            self._state_duration = self._roll_duration()
            self._pick_next_state()

        if self._state is PetState.WALK:
            self._walk()

        self.update()

    def _walk(self) -> None:
        self._x += self._config.speed * self._direction

        if self._x <= self._min_x:
            self._x, self._direction = self._min_x, 1
        elif self._x >= self._max_x:
            self._x, self._direction = self._max_x, -1

        self.move(round(self._x), self._y)

    # ---------------------------------------------------------------- painting

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        painter = QPainter(self)
        painter.scale(self._config.scale, self._config.scale)
        draw_pet(
            painter,
            self._state,
            self._direction,
            self._frame,
            self._config.palette,
        )
        painter.end()
