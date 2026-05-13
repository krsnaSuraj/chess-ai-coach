<div align="center">

# ♟️ Chess Coach

**Real-time chess analysis tool powered by Stockfish engine**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)](https://www.riverbankcomputing.com/software/pyqt/)
[![FastAPI](https://img.shields.io/badge/Web-FastAPI-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**Desktop GUI** · **Web App** · **Real-time Analysis** · **Blunder Detection**

</div>

---

## 📌 What is this?

A tool that uses the **Stockfish chess engine** to analyze your games in real-time.   
It shows the best move, evaluation score, blunders, and more — through a clean desktop or web interface.

**This is NOT AI.** It uses Stockfish — a traditional chess engine based on calculation, not machine learning.

---

## 🚀 Quick Start

### One-click setup (Windows)
Double-click **`install.bat`** — it will auto-install everything.

### Manual setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run
python run.py          # Desktop mode
python run.py web      # Web mode (works on mobile too)
```

**Desktop mode** opens a full window with a dashboard on the side.  
**Web mode** starts a local server — open http://localhost:8000 in any browser.

---

## 🎮 How to Play

| Step | What to Do |
|---|---|
| **1** | Choose White or Black at the start |
| **2** | Drag pieces to make moves (you play both sides) |
| **3** | Stockfish analyzes on YOUR turn |
| **4** | Check the dashboard for suggestions |

The idea is simple: play on chess.com on your phone, enter the same moves here, and use the Stockfish suggestions to decide your next move.

---

## ✨ Features

| Feature | What It Does |
|---|---|
| 🤖 **Engine Analysis** | Stockfish evaluates every position in real-time (depth 20+) |
| 🎯 **Best Move Arrow** | Green arrow on the board shows the recommended move |
| 📊 **Evaluation Bar** | Gradient bar — green = equal, red = advantage |
| ⚠️ **Blunder Detection** | Alerts when a move worsens the position by 1.0+ pawns |
| 👑 **Check Detection** | Red highlight on the king when in check |
| 🔄 **Last Move Highlight** | Yellow highlight on the most recent move |
| ⚪ **Legal Move Indicators** | Dots for valid moves, rings for captures |
| 📜 **Move History** | Complete move list in algebraic notation in the sidebar |
| 💬 **Coach Feedback** | Position assessment with descriptions |
| 🖱️ **Drag & Drop** | Smooth piece dragging with semi-transparent shadow |

---

## 📁 Project Files Explained

```
chess-coach/
├── run.py              ← The ONLY file you need to run
├── server.py           ← Web server code (used with "python run.py web")
├── board_gui.py        ← Desktop window code (board, pieces, sidebar)
├── engine_handler.py   ← Connects to Stockfish engine for analysis
├── stockfish.exe       ← Stockfish chess engine (76 MB, included)
├── config.yaml         ← Settings (engine speed, board colors)
├── requirements.txt    ← List of required Python packages
├── UPDATE.bat          ← For publishing updates to GitHub
├── README.md           ← This file
└── static/             ← Web files (HTML, images) for browser mode
```

---

## 📱 Web Mode on Mobile

```bash
python run.py web
```

Find your computer's local IP:
```bash
ipconfig
# Look for: IPv4 Address: 192.168.x.x
```

On your phone browser, open:
```
http://192.168.x.x:8000
```

Both devices must be on the same WiFi network.

---

## ⚙️ Settings (config.yaml)

```yaml
engine:
  threads: 2          # CPU cores to use (higher = faster analysis)
  hash: 1024          # Memory in MB for analysis
  movetime: 2000      # Time per move in milliseconds

display:
  dark_square: "#B58863"   # Dark square color
  light_square: "#F0D9B5"  # Light square color
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | Desktop GUI |
| [FastAPI](https://fastapi.tiangolo.com) | Web server |
| [Stockfish](https://stockfishchess.org) | Chess engine (analysis) |
| [python-chess](https://python-chess.readthedocs.io) | Chess logic & engine communication |
| [chessboard.js](https://chessboardjs.com) | Web chessboard UI |
| [chess.js](https://github.com/jhlywa/chess.js) | Web chess logic |

---

## ❓ Common Problems

| Problem | Solution |
|---|---|
| `pip install` fails | Make sure Python 3.10+ is installed |
| `Module not found` error | Run `pip install -r requirements.txt` again |
| Web page not loading | Use `http://localhost:8000` (not `https`) |
| Engine not analyzing | Check that `stockfish.exe` exists in the folder |
| `Permission denied` on Linux | Run `chmod +x stockfish` |
| Port already in use | Use a different port: `python run.py web 8080` |

---

## 📝 License

Open source under the MIT License.  
Stockfish is distributed under GPLv3.

---

<div align="center">

**Made for the chess community**

[Report Bug](https://github.com/krsnaSuraj/chess-coach/issues) · [Request Feature](https://github.com/krsnaSuraj/chess-coach/issues)

</div>
