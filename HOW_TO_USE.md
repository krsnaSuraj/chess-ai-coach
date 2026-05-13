# Chess AI Coach

A professional chess coaching application powered by Stockfish.
Available as a **Desktop GUI** (PyQt6) and **Web App** (FastAPI).

---

## Quick Start

```bash
pip install -r requirements.txt
```

### Desktop Mode
```bash
python run.py
```

### Web Mode
```bash
python run.py web
# Custom port:
python run.py web 8080
```
Open http://localhost:8000 in your browser.

---

## Features

| Feature | Description |
|---|---|
| **Real Piece Images** | Wikipedia-style piece set for both desktop and web |
| **Engine Analysis** | Stockfish evaluates every position in real-time |
| **Best Move Arrow** | Green arrow shows recommended move on the board |
| **Evaluation Bar** | Gradient bar (green=equal, red=advantage) |
| **Blunder Detection** | Alerts when position worsens by 1.0+ pawns |
| **Check Detection** | Red highlight on king in check |
| **Last Move Highlight** | Yellow highlight on last played move |
| **Legal Move Indicators** | Dots for moves, rings for captures |
| **Move History** | SAN notation with move numbers |
| **Coach Feedback** | Position assessment + blunder alerts |
| **Drag & Drop** | Smooth piece dragging with semi-transparent shadow |

---

## Controls

- **Desktop**: Click and drag pieces. Sidebar shows coach data.
- **Web**: Same drag-and-drop. Status bar shows coach data.

After selecting your color, play both sides — Stockfish only gives advice
during YOUR turn.

---

## Requirements

- **Python 3.10+**
- **Stockfish** (`stockfish.exe` included, 76 MB)
- **PyQt6** — Desktop GUI
- **python-chess** — Chess logic & UCI
- **PyYAML** — Config loader
- **FastAPI / Uvicorn** — Web server
- **Pydantic** — API models

---

## Project Structure

```
chess/
├── run.py              # Launcher (desktop / web)
├── main.py             # Desktop entry point
├── server.py           # Web server (FastAPI)
├── board_gui.py        # Desktop GUI (PyQt6)
├── engine_handler.py   # Stockfish thread manager
├── utils.py            # Config loader
├── config.yaml         # Settings
├── stockfish.exe       # Chess engine
├── HOW_TO_USE.md       # This file
├── requirements.txt
└── static/
    ├── index.html
    ├── js/             # chess.js, chessboard.js, jquery
    ├── css/            # chessboard.css
    └── img/chesspieces/wikipedia/   # 12 piece PNGs
```

---

## Configuration

Edit `config.yaml`:

```yaml
engine:
  path: "stockfish.exe"  # Engine binary
  threads: 2             # CPU threads
  hash: 1024             # Hash size (MB)
  movetime: 2000         # Analysis time (ms)

display:
  dark_square: "#B58863"
  light_square: "#F0D9B5"
  arrow_color: "#00FF00"
  arrow_opacity: 0.6
```

---

## Troubleshooting

**Q: Desktop app doesn't open?**
Make sure you have PyQt6 installed and a display connected.

**Q: Web server shows "Connection Error"?**
Ensure Stockfish is present at the path in `config.yaml` and port 8000 is free.

**Q: Engine analysis is slow?**
Reduce `movetime` in config.yaml or increase `threads` (max = CPU cores).
