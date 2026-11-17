"""Command-line entry point and system tray integration."""

import argparse
import signal
import sys
from dataclasses import replace
from typing import Optional, Sequence

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon

from . import __version__
from .config import BASE_SIZE, PetConfig, PetState
from .pet import DesktopPet
from .renderer import draw_pet


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="desktop-pet",
        description="A tiny click-through cat that wanders along the bottom of your screen.",
    )
    parser.add_argument("--scale", type=float, default=1.0, help="size multiplier (default: 1.0)")
    parser.add_argument("--speed", type=float, default=2.0, help="walking speed in px/tick (default: 2.0)")
    parser.add_argument("--fps", type=int, default=30, help="frames per second (default: 30)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    if args.scale <= 0:
        parser.error("--scale must be greater than 0")
    if args.speed < 0:
        parser.error("--speed must not be negative")
    if args.fps < 1:
        parser.error("--fps must be at least 1")
    return args


def _make_tray_icon() -> QIcon:
    pixmap = QPixmap(BASE_SIZE, BASE_SIZE)
    pixmap.fill(0)  # fully transparent
    painter = QPainter(pixmap)
    draw_pet(painter, PetState.IDLE, 1, 0)
    painter.end()
    return QIcon(pixmap)


def _build_tray(app: QApplication, pet: DesktopPet) -> Optional[QSystemTrayIcon]:
    """The pet ignores mouse input, so the tray icon is the way to pause or quit."""
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray not available; press Ctrl+C in the terminal to quit.", file=sys.stderr)
        return None

    tray = QSystemTrayIcon(_make_tray_icon(), app)
    tray.setToolTip("Desktop Pet")

    menu = QMenu()
    pause_action = QAction("Pause", menu, checkable=True)
    pause_action.toggled.connect(pet.set_paused)
    quit_action = QAction("Quit", menu)
    quit_action.triggered.connect(app.quit)
    menu.addAction(pause_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()
    tray._menu = menu  # keep a reference so it is not garbage-collected
    return tray


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    config = replace(PetConfig(), scale=args.scale, speed=args.speed, fps=args.fps)

    app = QApplication(sys.argv[:1])
    app.setQuitOnLastWindowClosed(False)

    # Let Ctrl+C work: Python only handles signals while the interpreter runs,
    # so wake it up periodically.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    wake = QTimer()
    wake.start(500)
    wake.timeout.connect(lambda: None)

    pet = DesktopPet(config)
    pet.show()
    tray = _build_tray(app, pet)  # noqa: F841 (must stay referenced)

    return app.exec_()
