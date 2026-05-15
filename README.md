<div align="center">

# ♟️ Chess Coach

**Real-time chess analysis tool powered by Stockfish engine**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)](https://www.riverbankcomputing.com/software/pyqt/)
[![FastAPI](https://img.shields.io/badge/Web-FastAPI-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**Desktop GUI · Web App · Real-time Analysis · Blunder Detection**

</div>

---

## 🎯 What is this?

A tool that uses the **Stockfish chess engine** to analyze your chess games in real-time.  
Supports both **desktop GUI (PyQt6)** and **web interface (FastAPI)**.

---

## 📸 Screenshots

<p align="center">
  <img src="screenshots/Side-by-side.png" width="400" alt="Chess Analysis"/>
  <img src="screenshots/Server .png" width="400" alt="Web Server"/>
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time Analysis** | Stockfish engine evaluates positions instantly |
| **Blunder Detection** | Highlights mistakes, misses, and best moves |
| **Desktop GUI** | PyQt6-based native interface |
| **Web Interface** | FastAPI server — analyze from any browser |
| **Custom Engine Config** | Adjust depth, threads, hash size |
| **PGN Support** | Load/save games in standard PGN format |
| **Move Suggestions** | Top engine lines with evaluation |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Stockfish engine (included: `stockfish.exe`)

### Installation
```bash
git clone https://github.com/krsnaSuraj/chess-coach.git
cd chess-coach

# Install dependencies
pip install -r requirements.txt

# Run desktop GUI
python run.py

# Or run web server
python server.py
```

### Windows One-Click Install
```
Double-click install.bat
Then run.bat to start
```

---

## 🖥️ Usage

### Desktop GUI
```bash
python run.py
```
Opens the PyQt6 desktop application. Load a PGN or start a new analysis.

### Web Server
```bash
python server.py
```
Starts a FastAPI server at `http://localhost:8000`.  
Open your browser and start analyzing.

### Configuration
Edit `config.yaml` to customize:
- Stockfish path and parameters
- Analysis depth and threads
- Theme and display options

---

## 🏗️ Project Structure

```
chess-coach/
├── run.py                  # Desktop GUI entry point
├── server.py               # Web server (FastAPI)
├── board_gui.py            # PyQt6 chess board widget
├── engine_handler.py       # Stockfish engine wrapper
├── utils.py                # Helper functions
├── config.yaml             # User configuration
├── stockfish.exe           # Stockfish engine binary
├── requirements.txt        # Python dependencies
├── install.bat             # Windows installer
├── UPDATE.bat              # Version bump + push
├── screenshots/            # App screenshots
└── README.md               # This file
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| GUI Framework | PyQt6 |
| Web Framework | FastAPI + Uvicorn |
| Chess Engine | Stockfish (UCI protocol) |
| Analysis | Real-time evaluation, best line suggestions |

---

## 🔧 Configuration

```yaml
# config.yaml
engine:
  path: stockfish.exe
  depth: 20
  threads: 4
  hash: 256

display:
  theme: default
  show_eval_bar: true
  highlight_best_move: true

analysis:
  auto_analyze: true
  blunder_threshold: 300  # centipawn loss
```

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <a href="https://github.com/krsnaSuraj/chess-coach">github.com/krsnaSuraj/chess-coach</a>
</p>
