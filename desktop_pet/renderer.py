"""Stateless drawing code for the pet sprite."""

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen

from .config import ANIM_HALF, Palette, PetState


def _color(rgb) -> QColor:
    return QColor(*rgb)


def draw_pet(
    painter: QPainter,
    state: PetState,
    direction: int,
    frame: int,
    palette: Palette = Palette(),
) -> None:
    """Draw the cat into a 64x64 logical canvas.

    direction: 1 = facing right, -1 = facing left
    frame:     current animation tick (0 .. ANIM_FRAMES - 1)
    """
    painter.setRenderHint(QPainter.Antialiasing)

    first_half = frame < ANIM_HALF
    walking = state is PetState.WALK
    sleeping = state is PetState.SLEEP

    bounce = -3 if (walking and first_half) else 0
    body = _color(palette.body)
    outline = _color(palette.outline)
    eye = _color(palette.sleeping_eye) if sleeping else outline

    painter.setPen(QPen(outline, 2))
    painter.setBrush(QBrush(body))

    # Body
    body_y = 26 + bounce
    painter.drawRoundedRect(16, body_y, 32, 24, 10, 10)

    # Head (shifts slightly with direction)
    head_x = 24 if direction == 1 else 14
    head_y = 14 + bounce
    painter.drawEllipse(head_x, head_y, 26, 22)

    # Ears
    if direction == 1:
        ears = (
            ((4, 4), (8, -6), (14, 2)),
            ((14, 2), (20, -6), (23, 5)),
        )
    else:
        ears = (
            ((3, 5), (6, -6), (12, 2)),
            ((12, 2), (18, -6), (22, 4)),
        )
    for ear in ears:
        painter.drawPolygon(*(QPoint(head_x + dx, head_y + dy) for dx, dy in ear))

    # Eyes
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(eye))
    eye_offset = 6 if direction == 1 else 2
    left_eye_x = head_x + eye_offset + 2
    right_eye_x = head_x + eye_offset + 11
    if sleeping:
        painter.drawRect(left_eye_x, head_y + 10, 5, 2)
        painter.drawRect(right_eye_x, head_y + 10, 5, 2)
    else:
        painter.drawEllipse(left_eye_x, head_y + 8, 4, 5)
        painter.drawEllipse(right_eye_x, head_y + 8, 4, 5)

    # Tail
    painter.setPen(QPen(outline, 3))
    tail_x = 16 if direction == 1 else 48
    tail_end_x = tail_x - 10 * direction
    tail_wag = 4 if first_half else -4
    painter.drawLine(tail_x, body_y + 14, tail_end_x, body_y + 4 + tail_wag)

    # Paws
    painter.setPen(QPen(outline, 2))
    painter.setBrush(QBrush(body))
    if walking:
        leg_offset = 3 if first_half else -3
    else:
        leg_offset = 0
    painter.drawEllipse(20 + leg_offset, 48, 8, 6)
    painter.drawEllipse(36 - leg_offset, 48, 8, 6)
