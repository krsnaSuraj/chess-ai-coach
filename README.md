<div align="center">

# ♟️ Chess Coach

**A real-time chess analysis tool powered by the Stockfish engine**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)](https://www.riverbankcomputing.com/software/pyqt/)
[![FastAPI](https://img.shields.io/badge/Web-FastAPI-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**Desktop GUI** · **Web App** · **Real-time Analysis** · **Blunder Detection**

---

</div>

## 📋 Overview

Chess Coach is a real-time chess analysis tool. It uses the **Stockfish engine** to evaluate positions, suggest moves, detect blunders, and provide instant feedback — without any AI or machine learning, just raw engine calculation.

Available as both a **desktop application** (PyQt6) and a **web application** (FastAPI) that works on mobile devices.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Engine Analysis** | Stockfish evaluates every position in real-time (depth 20+) |
| 🎯 **Best Move Arrow** | Green arrow shows the recommended move on the board |
| 📊 **Evaluation Bar** | Gradient bar — green for equal, red shows advantage |
| ⚠️ **Blunder Detection** | Alerts when a move worsens the position by 1.0+ pawns |
| 👑 **Check Detection** | Red highlight on the king when in check |
| 🔄 **Last Move Highlight** | Yellow highlight on the most recent move |
| ⚪ **Legal Move Indicators** | Dots for valid moves, rings for captures |
| 📜 **Move History** | Complete move list in standard algebraic notation |
| 💬 **Coach Feedback** | Position assessment with advantage descriptions |
| 🖱️ **Drag & Drop** | Smooth piece dragging with semi-transparent shadow |

---

## 🎬 Workflow

```
1. Choose your color (White/Black)
         │
         ▼
2. Play moves for both sides
         │
         ├── Your turn → Stockfish analyzes → Shows best move + eval
         │
         └── Opponent's turn → Enter their move → No suggestions
         │
         ▼
3. Use the suggestion on chess.com or any chess platform
```

> **Pro tip:** Play on chess.com on your phone, enter the same moves here, and use the engine suggestions to decide your next move.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Stockfish (included — `stockfish.exe`, 76 MB)

### Installation

```bash
# Clone the repository
git clone https://github.com/krsnaSuraj/chess-ai-coach.git
cd chess-ai-coach

# Install dependencies
pip install -r requirements.txt

# Run desktop app
python run.py

# Or run web app (mobile-friendly)
python run.py web
```

---

## 🖥️ Desktop App

The main interface with a full-featured dashboard.

```
┌─────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────────────────────┐ │
│  │              │  │       COACH DASHBOARD         │ │
│  │   Chess      │  │  ┌─────┐                     │ │
│  │   Board      │  │  │eval ├── Evaluation: +0.35 │ │
│  │   with       │  │  │ bar │── Best Move: e2e4   │ │
│  │   Piece      │  │  └─────┘── Engine: Depth 20  │ │
│  │   Images     │  │                              │ │
│  │              │  │  Coach Feedback              │ │
│  │   ← Arrow   │  │  ┌──────────────────────┐    │ │
│  │              │  │  │ White is better      │    │ │
│  └──────────────┘  │  └──────────────────────┘    │ │
│                    │  Move History                │ │
│                    │  ┌──────────────────────┐    │ │
│                    │  │ 1W  e4               │    │ │
│                    │  │ 1B  e5               │    │ │
│                    │  └──────────────────────┘    │ │
│                    └──────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Controls
- **Click & drag** pieces to make moves
- **Sidebar** shows all coach data (evaluation, best move, feedback)
- **Status bar** at the bottom shows engine status

---

## 🌐 Web App

Runs in any browser — desktop or mobile.

```bash
python run.py web
# Open: http://localhost:8000
```

- Same features as the desktop app
- Mobile-friendly with touch support
- Wikipedia-style piece images
- Green arrow for best move recommendations

---

## ⚙️ Configuration

Edit `config.yaml` to customize the engine and display settings:

```yaml
engine:
  path: "stockfish.exe"   # Path to Stockfish binary
  threads: 2              # CPU threads for analysis
  hash: 1024              # Hash table size (MB)
  movetime: 2000          # Analysis time per move (ms)

display:
  dark_square: "#B58863"  # Dark square color
  light_square: "#F0D9B5" # Light square color
  arrow_color: "#00FF00"  # Best move arrow color
```

---

## 📂 Project Structure

```
chess-ai-coach/
├── run.py              # Launcher (desktop / web)
├── main.py             # Desktop entry point
├── server.py           # Web server (FastAPI)
├── board_gui.py        # Desktop GUI (PyQt6)
├── engine_handler.py   # Stockfish engine manager
├── utils.py            # Configuration loader
├── config.yaml         # Engine & display settings
├── stockfish.exe       # Stockfish chess engine
├── UPDATE.bat          # GitHub update tool
├── requirements.txt
├── README.md
└── static/             # Web frontend
    ├── index.html
    ├── js/
    ├── css/
    └── img/chesspieces/wikipedia/
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | Desktop graphical user interface |
| [FastAPI](https://fastapi.tiangolo.com) | Web server framework |
| [Stockfish](https://stockfishchess.org) | UCI chess engine |
| [python-chess](https://python-chess.readthedocs.io) | Chess logic and UCI protocol |
| [chessboard.js](https://chessboardjs.com) | Web chessboard UI |
| [chess.js](https://github.com/jhlywa/chess.js) | Web chess logic |

---

## 📝 License

This project is open source and available under the MIT License.

Stockfish is distributed under the GPLv3 license.

---

<div align="center">

**Made with ❤️ for the chess community**

[Report Bug](https://github.com/krsnaSuraj/chess-ai-coach/issues) · [Request Feature](https://github.com/krsnaSuraj/chess-ai-coach/issues)

</div>
