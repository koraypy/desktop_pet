# 🐈‍⬛ Desktop Pet

A tiny neon-outlined black cat that wanders along the bottom of your screen.
It walks, idles and naps, always stays on top, and **never blocks your clicks**.

🇹🇷 [Türkçe](README.tr.md)

## Features

- Frameless, transparent, always-on-top window
- Click-through: it never gets in the way of your work
- Random behaviour: walking, idling, sleeping
- System tray menu to pause or quit
- Adjustable size, speed and frame rate

## Installation

Requires Python 3.9+.

```bash
git clone https://github.com/koraypy/desktop-pet.git
cd desktop-pet
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python -m desktop_pet
```

Options:

| Option    | Default | Description                    |
|-----------|---------|--------------------------------|
| `--scale` | `1.0`   | Size multiplier                |
| `--speed` | `2.0`   | Walking speed (pixels per tick)|
| `--fps`   | `30`    | Animation frames per second    |

Example: `python -m desktop_pet --scale 1.5 --speed 3`

Or install it as a command: `pip install .` then run `desktop-pet`.

## Controls

The pet ignores mouse input by design. Use the **system tray icon** to
pause or quit, or press `Ctrl+C` in the terminal.

## Platform notes

- **Windows / X11**: fully supported.
- **macOS**: works; the tray icon appears in the menu bar.
- **Linux (Wayland)**: "always on top" and click-through may be limited by the
  compositor. Try `QT_QPA_PLATFORM=xcb python -m desktop_pet`.
- Only the primary screen is used.

## Customising

- Colours, behaviour weights and durations: `desktop_pet/config.py`
- Sprite drawing: `desktop_pet/renderer.py`

## Project structure

```
desktop_pet/
├── app.py        # CLI + system tray
├── config.py     # constants and settings
├── pet.py        # window, movement, behaviour
└── renderer.py   # sprite drawing
```

## License

[MIT](LICENSE)
