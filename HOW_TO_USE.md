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

## How It Works

1. Select your color (White or Black)
2. Play both sides — Stockfish only gives advice during your turn
3. The dashboard shows evaluation, best move, and coach feedback

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

## Configuration

Edit `config.yaml`:

```yaml
engine:
  path: "stockfish.exe"
  threads: 2
  hash: 1024
  movetime: 2000

display:
  dark_square: "#B58863"
  light_square: "#F0D9B5"
  arrow_color: "#00FF00"
  arrow_opacity: 0.6
```

---

## Publishing to GitHub

### First Time
1. Create a repository on GitHub named `chess-ai-coach`
2. Double-click `UPDATE.bat` in the project folder
3. Paste your GitHub repository URL when prompted

### Future Updates
After making code changes, double-click `UPDATE.bat`:
- It will detect all changes
- Commit and push to GitHub automatically

---

## Project Structure

```
chess-ai-coach/
├── run.py              # Launcher (desktop / web)
├── main.py             # Desktop entry point
├── server.py           # Web server (FastAPI)
├── board_gui.py        # Desktop GUI (PyQt6)
├── engine_handler.py   # Stockfish thread manager
├── utils.py            # Config loader
├── config.yaml         # Settings
├── stockfish.exe       # Chess engine
├── UPDATE.bat          # GitHub update tool
├── HOW_TO_USE.md       # This file
├── requirements.txt
└── static/
    ├── index.html
    ├── js/
    ├── css/
    └── img/chesspieces/wikipedia/
```

---

## Troubleshooting

**Desktop app doesn't open?**
Ensure PyQt6 is installed and a display is connected.

**Web server shows "Connection Error"?**
Check that Stockfish is at the path in `config.yaml` and port 8000 is free.

**Engine analysis is slow?**
Reduce `movetime` in config.yaml or increase `threads` (max = CPU cores).
