<div align="center">

# ♟️ Chess Coach

**Real-time position analysis engine · Desktop GUI & Web Interface**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![FastAPI](https://img.shields.io/badge/Web-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Stockfish](https://img.shields.io/badge/Engine-Stockfish_17-FF6600?logo=chess&logoColor=white)](https://stockfishchess.org)
[![License](https://img.shields.io/badge/license-MIT-808080)](LICENSE)

[Features](#-features) · [Quick Start](#-quick-start) · [Usage](#-usage) · [Configuration](#%EF%B8%8F-configuration) · [Architecture](#-architecture) · [Tech Stack](#-tech-stack)

</div>

---

## 🎯 Overview

Chess Coach is a real-time chess analysis sidekick that integrates **Stockfish 17** into a dual-interface application. It evaluates positions as *you* play your selected side, detects blunders, suggests best moves, and presents principal variation lines — while staying silent when you manually enter opponent moves.

**Perfect for:** Online chess (chess.com, lichess) where you play one side and want expert guidance without distraction.

Choose your interface:

| Interface | Use Case |
|-----------|----------|
| **Desktop GUI** (PyQt6) | Full-featured analysis with eval bar, coach dashboard, and move history |
| **Web Interface** (FastAPI) | Lightweight browser-based access — play on PC, analyze on phone (same LAN) |

---

## ✨ Features

<table>
  <tr>
    <td>
      <h4>🧑‍🤝‍🧑 Single-Side Sidekick</h4>
      Select your side (White/Black). Coach analyzes only your moves. You manually enter opponent moves — coach stays silent during opponent's turn.
    </td>
    <td>
      <h4>🎯 Unrestricted Dragging</h4>
      Drag any piece at any time. Legal move validation handled by engine. Perfect for entering opponent's moves on the board.
    </td>
  </tr>
  <tr>
    <td>
      <h4>⚡ Real-time Evaluation</h4>
      Continuous Stockfish analysis updates eval, depth, and principal variation as you play.
    </td>
    <td>
      <h4>🚨 Blunder Detection</h4>
      Instantly flags moves that lose ≥1.0 pawns of advantage compared to the previous position.
    </td>
  </tr>
  <tr>
    <td>
      <h4>🎯 Best Move Suggestion</h4>
      Visual arrow overlay and UCI display showing the top engine line for the current position.
    </td>
    <td>
      <h4>📊 Coach Dashboard</h4>
      Eval bar, advantage label, engine depth, PV line, and natural-language feedback panel (desktop).
    </td>
  </tr>
  <tr>
    <td>
      <h4>↩️ Undo / Redo</h4>
      Full move-history navigation with Ctrl+Z / Ctrl+Y shortcuts on both desktop and web.
    </td>
    <td>
      <h4>🌐 LAN Multi-device</h4>
      Web server auto-detects your LAN IP — analyze on your phone while the engine runs on your PC.
    </td>
  </tr>
  <tr>
    <td>
      <h4>⚙️ Configurable Engine</h4>
      Tweak Stockfish threads, hash size, and analysis time via <code>config.yaml</code>.
    </td>
    <td>
      <h4>🔄 Analysis Cache</h4>
      Smart caching eliminates redundant engine calls when reviewing positions.
    </td>
  </tr>
</table>

---

## 📸 Screenshots

<p align="center">
  <img src="screenshots/Side-by-side.png" width="420" alt="Desktop GUI — Coach Dashboard"/>
  <img src="screenshots/Server .png" width="420" alt="Web Interface"/>
</p>

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Stockfish 17** — download from [stockfishchess.org](https://stockfishchess.org/download/)

### One-Click Setup (Windows)

1. Clone the repo: `git clone https://github.com/krsnaSuraj/chess-coach.git && cd chess-coach`
2. **Double-click `install.bat`** (or run `python install.bat` manually)
3. Download Stockfish and place `stockfish.exe` in the project root
4. Done! Run the app below

### Manual Setup (All Platforms)

For detailed installation instructions for Windows, macOS, and Linux, see **[INSTALLATION.md](INSTALLATION.md)**

### Launch

```bash
# Desktop GUI
python run.py

# Web server (http://localhost:8000)
python run.py web
python run.py web 8080    # custom port
```

---

## 🖥️ Usage

### Desktop GUI Workflow

1. Run `python run.py`
2. Select your color — **White** or **Black** (your side in the online game)
3. Play your move → coach analyzes and displays best move + feedback
4. Opponent moves online → **drag their pieces on the app to record the move**
5. Coach shows "Waiting — *Color*'s turn" during opponent's turn (no analysis)
6. Repeat until game ends
7. Use **Undo** / **Redo** buttons or `Ctrl+Z` / `Ctrl+Y` to navigate history
8. **New Game** restarts with a fresh color choice

**Key Insight:** You can drag *any* piece at *any* time (unrestricted), so entering opponent moves is seamless. The coach simply won't analyze during opponent's turn.

The sidebar shows:

| Panel | Content | Shows When |
|-------|---------|-----------|
| **Turn Indicator** | Current side to move, check/checkmate status | Always |
| **Evaluation** | Numeric eval (centipawns), colored eval bar, advantage label | Your turn only |
| **Best Line** | Top engine move and 4-ply principal variation | Your turn only |
| **Coach Feedback** | Natural-language position assessment + blunder alerts | Your turn only |
| **Move History** | Annotated move list with SAN notation | Always |

### Web Interface Workflow

Same chess logic, served over HTTP:

1. Run `python run.py web` (or `python run.py web 8080` for a custom port)
2. Open **http://localhost:8000** in your browser (or the LAN URL for other devices)
3. Select your color
4. Play as above — drag pieces freely to enter both your moves and opponent's moves
5. Coach analysis appears only during your turn
6. Undo / Redo via buttons or keyboard shortcuts

The web frontend uses [chessboard.js](https://chessboardjs.com/) and [chess.js](https://github.com/jhlywa/chess.js) for drag-and-drop interaction. Analysis results are returned with every move via FastAPI endpoints — no polling required.

---

## 💡 The Sidekick Workflow

**Typical online chess session with Chess Coach:**

```
You (Playing Online at chess.com, lichess, etc.)          Chess Coach App
─────────────────────────────────────────────────────────────────────────
Play move (e.g., 1.e4)                                   → [Coach analyzes]
                                                         → "Best: e4, Position equal"
                                                         
Opponent plays (e.g., ...c5)                             [You drag c7→c5]
                                                         [Coach says "Waiting — Black's turn"]
                                                         (No analysis during opponent's turn)
                                                         
Play move (e.g., 2.Nf3)                                  → [Coach analyzes]
                                                         → "Best: Nf3, You're better"
                                                         
Opponent plays (e.g., ...d6)                             [You drag d7→d6]
                                                         [Coach stays silent]
                                                         
[… game continues …]
```

**Why this design?**

- **Focus:** No distraction during opponent's turn — the app doesn't bombard you with position evals while they're thinking
- **Learning:** Coach suggests your moves, but opponent's moves are your responsibility (you enter them manually)
- **Flexibility:** Unrestricted dragging lets you enter any move instantly without frustration

---

## ⚙️ Configuration

Edit `config.yaml` in the project root:

```yaml
engine:
  path: "stockfish.exe"        # Path to Stockfish binary
  threads: 2                    # Engine CPU threads
  hash: 64                      # Hash table size in MB
  movetime: 2000                # Desktop analysis time (ms)
  web_movetime: 0.15            # Web analysis time (seconds)

display:
  dark_square: "#B58863"
  light_square: "#F0D9B5"
  arrow_color: "#00FF00"
  arrow_opacity: 0.6
```

### Tuning Tips

- **Reduce `web_movetime`** for snappier web responses (min ~0.05s).
- **Increase `hash`** for deeper analysis on systems with ample RAM (256–1024 MB).
- **Increase `threads`** to match your CPU core count for faster evaluation.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Chess Coach                        │
│                                                      │
│  ┌──────────────┐     ┌──────────────────────────┐  │
│  │  Desktop GUI  │     │     Web Server           │  │
│  │   (PyQt6)     │     │   (FastAPI + Uvicorn)    │  │
│  │               │     │                          │  │
│  │  ChessBoard   │     │  /api/start_game  POST   │  │
│  │  ─ drag/drop  │     │  /api/human_move  POST   │  │
│  │  ─ eval bar   │     │  /api/game_state  GET    │  │
│  │  ─ highlights │     │  /api/undo        POST   │  │
│  │  ─ arrow      │     │  /api/redo        POST   │  │
│  │               │     │  /api/health      GET    │  │
│  │  MainWindow   │     │  static/ (frontend)      │  │
│  │  ─ dashboard  │     └──────────┬───────────────┘  │
│  │  ─ feedback   │                │                  │
│  │  ─ move list  │                │                  │
│  └───────┬───────┘                │                  │
│          │                        │                  │
│          └──────────┬─────────────┘                  │
│                     │                                │
│          ┌──────────▼──────────┐                     │
│          │   GameController    │                     │
│          │  ─ board state      │                     │
│          │  ─ move validation  │                     │
│          │  ─ undo/redo stack  │                     │
│          │  ─ analysis cache   │                     │
│          └──────────┬──────────┘                     │
│                     │                                │
│          ┌──────────▼──────────┐                     │
│          │  Stockfish Engine   │                     │
│          │  ─ UCI protocol     │                     │
│          │  ─ async analysis   │                     │
│          │  ─ eval extraction  │                     │
│          └─────────────────────┘                     │
└─────────────────────────────────────────────────────┘
```

### Data Flow

1. **User moves** a piece (desktop drag or web click) — any piece, any time (unrestricted dragging)
2. **Move is validated** against legal moves by the chess engine
3. **Board state updates** and analysis cache invalidates
4. **Coach decision:** Is it the user's selected side's turn?
   - ✅ **YES** → Engine analyzes the position; returns eval, best move, PV, depth, blunder check
   - ❌ **NO** → Coach silent; board updates without analysis (waiting state)
5. **UI updates** with analysis or "Waiting" message depending on whose turn it is
6. **Blunder detection** (only on user's turn) compares current eval vs. previous position eval

---

## 📁 Project Structure

```
chess-coach/
├── 📄 run.py                    # Launcher (desktop or web mode)
├── 📄 server.py                 # FastAPI web server + GameController
├── 📄 board_gui.py              # PyQt6 desktop GUI (board + dashboard)
├── 📄 engine_handler.py         # Stockfish engine wrapper + threading
├── 📄 utils.py                  # Config loader
│
├── ⚙️ config.yaml               # Engine & display settings
├── 📋 requirements.txt          # Python package dependencies
├── 📋 INSTALLATION.md           # Detailed setup guide (Windows/macOS/Linux)
├── 📋 README.md                 # This file
├── 📋 LICENSE                   # MIT License
├── 📋 .gitignore                # Git ignore rules
│
├── 🪟 install.bat               # Windows one-click installer
├── 🪟 UPDATE.bat                # Windows update helper
├── 📦 stockfish.exe             # Stockfish 17 binary (user-provided)
│
├── 🗂️ .venv/                     # Virtual environment (created by install)
├── 🗂️ __pycache__/              # Python cache (auto-generated)
│
├── 🗂️ static/                    # Web frontend
│   ├── 📄 index.html            # Main web page
│   ├── 🗂️ css/
│   │   └── chessboard.css       # Chessboard styles
│   ├── 🗂️ js/
│   │   ├── chessboard.js        # Chessboard library
│   │   ├── chess.js             # Chess logic library
│   │   └── jquery.min.js        # jQuery library
│   └── 🗂️ img/
│       └── 🗂️ chesspieces/
│           └── 🗂️ wikipedia/    # Piece images (PNG)
│               ├── wP.png, wN.png, wB.png, wR.png, wQ.png, wK.png
│               └── bP.png, bN.png, bB.png, bR.png, bQ.png, bK.png
│
└── 🗂️ screenshots/              # App screenshots
    ├── Side-by-side.png         # Desktop GUI
    └── Server.png               # Web interface
```

For detailed setup and folder navigation, see **[INSTALLATION.md](INSTALLATION.md)**

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Language** | Python 3.10+ | Core logic and glue |
| **Desktop UI** | PyQt6 | Native chess board, drag-and-drop, sidebar widgets |
| **Web Framework** | FastAPI + Uvicorn | REST API, static file serving, CORS |
| **Engine Protocol** | python-chess (`chess.engine`) | UCI communication with Stockfish |
| **Web Frontend** | chessboard.js + chess.js | Browser-based board interaction |
| **Concurrency** | `threading` + `QThread` | Non-blocking engine analysis |
| **Configuration** | PyYAML | `config.yaml` parsing |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-idea`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feat/your-idea`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<p align="center">
  <a href="https://github.com/krsnaSuraj/chess-coach">
    <img src="https://img.shields.io/badge/-View_on_GitHub-181717?logo=github&logoColor=white" alt="GitHub">
  </a>
  <br>
  <sub>Built with ♟️ by <a href="https://github.com/krsnaSuraj">Krsna Suraj</a></sub>
</p>
