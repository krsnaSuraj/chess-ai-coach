# 🚀 Installation Guide - Chess Coach

**Quick Start Guide for Windows, macOS, and Linux**

---

## ⚡ Windows (Fastest Setup)

### Option 1: One-Click Setup (Recommended)

1. **Download** the project or clone it:
   ```bash
   git clone https://github.com/krsnaSuraj/chess-coach.git
   cd chess-coach
   ```

2. **Double-click** `install.bat` in the project folder
   - This will:
     - Check Python installation
     - Create virtual environment (`.venv`)
     - Install all dependencies
     - Verify Stockfish

3. **Download Stockfish 17** (if not found):
   - Download from: https://stockfishchess.org/download/
   - Extract and place `stockfish.exe` in the project root folder
   - Re-run `install.bat` to verify

4. **Run the app:**
   ```bash
   python run.py          # Desktop GUI
   python run.py web      # Web interface (http://localhost:8000)
   ```

---

### Option 2: Manual Setup (Windows)

1. **Verify Python 3.10+:**
   ```bash
   python --version
   ```
   If not installed: https://www.python.org/downloads/ (check "Add Python to PATH")

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Stockfish:**
   - https://stockfishchess.org/download/
   - Extract `stockfish.exe` to project root

5. **Run:**
   ```bash
   python run.py          # Desktop
   python run.py web      # Web
   ```

---

## 🍎 macOS / 🐧 Linux

### Prerequisites

- **Python 3.10+:** `python3 --version`
- **Stockfish 17:** 
  - macOS: `brew install stockfish`
  - Linux: `sudo apt-get install stockfish` (Ubuntu/Debian)
  - Or download from: https://stockfishchess.org/download/

### Setup Steps

1. **Clone project:**
   ```bash
   git clone https://github.com/krsnaSuraj/chess-coach.git
   cd chess-coach
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update Stockfish path** (if installed to non-default location):
   - Edit `config.yaml`:
     ```yaml
     engine:
       path: "/usr/games/stockfish"  # Linux example
       # or
       path: "/opt/homebrew/bin/stockfish"  # macOS example
     ```

5. **Run:**
   ```bash
   python run.py          # Desktop (requires X11 on Linux)
   python run.py web      # Web (recommended for Linux/server)
   ```

---

## ✅ Verification

After setup, verify everything works:

```bash
python -c "import chess, pyqt6, fastapi, yaml; print('All imports OK!')"
```

Check config:
```bash
python -c "from utils import load_config; print(load_config())"
```

Test desktop (if available):
```bash
python run.py
# Select White or Black, drag pieces to test
# Press Ctrl+Q to close
```

Test web:
```bash
python run.py web
# Open http://localhost:8000 in browser
# Select White or Black
# Drag pieces to test
```

---

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
engine:
  path: "stockfish.exe"      # Path to Stockfish binary
  threads: 2                  # CPU threads (match your CPU cores)
  hash: 64                    # RAM for analysis (MB): 64, 128, 256, 512, 1024
  movetime: 2000              # Desktop analysis time (milliseconds)
  web_movetime: 0.15          # Web analysis time (seconds)

display:
  dark_square: "#B58863"      # Board dark square color
  light_square: "#F0D9B5"     # Board light square color
  arrow_color: "#00FF00"      # Best move arrow color
  arrow_opacity: 0.6          # Arrow transparency (0.0-1.0)
```

### Tuning Tips

| Setting | Recommendation | Notes |
|---------|---|---|
| `threads` | Match CPU cores | 4 threads = quad-core, 8 threads = octa-core |
| `hash` | System RAM / 8 | 16GB RAM → 64-256MB safe; can go higher if needed |
| `movetime` (desktop) | 1000-5000 ms | Faster (1000) = snappier but less accurate |
| `web_movetime` | 0.1-0.5 s | Lower (0.1) = responsive; higher (0.5) = accurate |

---

## 📁 Folder Structure

```
chess-coach/
├── 📄 run.py                    # Launcher script (desktop or web)
├── 📄 server.py                 # FastAPI web server + game logic
├── 📄 board_gui.py              # PyQt6 desktop GUI
├── 📄 engine_handler.py         # Stockfish engine wrapper
├── 📄 utils.py                  # Configuration loader
├── 📄 config.yaml               # Settings (engine, display)
├── 📄 requirements.txt          # Python package dependencies
├── 📄 install.bat               # Windows one-click installer
├── 📄 UPDATE.bat                # Windows update helper
├── 📄 README.md                 # Project documentation
├── 📄 LICENSE                   # MIT License
├── 📄 .gitignore                # Git ignore rules
├── 🗂️ .venv/                     # Virtual environment (created by install)
├── 🗂️ __pycache__/              # Python cache (auto-generated)
├── 🗂️ static/                    # Web frontend files
│   ├── 📄 index.html            # Main web page
│   ├── 🗂️ css/
│   │   └── 📄 chessboard.css    # Board styles
│   ├── 🗂️ js/
│   │   ├── 📄 chessboard.js     # Board library
│   │   ├── 📄 chess.js          # Chess logic library
│   │   └── 📄 jquery.min.js     # jQuery library
│   └── 🗂️ img/
│       └── 🗂️ chesspieces/
│           └── 🗂️ wikipedia/    # Chess piece images
│               ├── wP.png, wN.png, wB.png, wR.png, wQ.png, wK.png
│               └── bP.png, bN.png, bB.png, bR.png, bQ.png, bK.png
├── 🗂️ screenshots/              # App preview images
│   ├── 📷 Side-by-side.png      # Desktop GUI screenshot
│   └── 📷 Server.png            # Web interface screenshot
└── 📦 stockfish.exe             # Stockfish 17 binary (user-provided)
```

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python: https://www.python.org/downloads/
- **Windows:** Check "Add Python to PATH" during installation
- **macOS:** Use Homebrew: `brew install python@3.10`
- **Linux:** `sudo apt-get install python3.10`

### "Stockfish not found"
- Download from: https://stockfishchess.org/download/
- **Windows:** Place `stockfish.exe` in project root
- **macOS/Linux:** Install via package manager or update `config.yaml` with full path

### "ModuleNotFoundError: No module named 'PyQt6'"
- Windows: Re-run `install.bat`
- macOS/Linux: `pip install PyQt6`

### "Web server won't start on port 8000"
- Port already in use → use custom port: `python run.py web 8080`

### "Engine is too slow"
- Increase `threads` in `config.yaml` (match your CPU cores)
- Increase `hash` in `config.yaml` (if you have RAM available)

### "Desktop GUI won't open"
- Linux users: Need X11 display server (GUI requires display)
- Solution: Use web interface instead: `python run.py web`

---

## 🚀 First Game

### Desktop Mode

1. Run: `python run.py`
2. Select **White** or **Black** (your side)
3. Drag pieces to play your moves
4. Coach shows: Best move, evaluation, analysis
5. When opponent moves (online): Drag their piece to update board
6. Coach stays silent on opponent's turn (you enter moves manually)

### Web Mode

1. Run: `python run.py web`
2. Open http://localhost:8000 (or LAN URL shown in terminal)
3. Select your color
4. Play same as desktop
5. Access from phone on same WiFi

---

## 💡 Tips

- **Online Chess:** Play on chess.com, lichess, etc. Use Chess Coach as sidekick on same PC/phone
- **Performance:** Increase `hash` if you have RAM; increase `threads` to match CPU
- **Phone Access:** Run `python run.py web` on PC, open `http://<YOUR_PC_IP>:8000` on phone (same WiFi)
- **Custom Stockfish:** Edit `config.yaml` to point to your Stockfish binary

---

## 📞 Support

- **GitHub Issues:** https://github.com/krsnaSuraj/chess-coach/issues
- **Stockfish Help:** https://stockfishchess.org/

---

**Happy analyzing!** ♟️
