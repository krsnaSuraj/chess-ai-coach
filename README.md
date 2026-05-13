# ♟️ Chess Coach

**Real-time chess analysis tool powered by Stockfish engine.**

Available in two modes:
- **Desktop App** — Full window with dashboard (recommended)
- **Web App** — Works in browser, also on mobile

---

## 🚀 How to Use

### Step 1: Install

```bash
pip install -r requirements.txt
```

### Step 2: Run

**Desktop mode** (recommended):
```bash
python run.py
```

**Web mode** (works on phone too):
```bash
python run.py web
```
Then open http://localhost:8000 in your browser.

### Step 3: Play

1. Choose White or Black
2. Drag pieces to make moves (you play both sides)
3. Stockfish analyzes and shows suggestions on YOUR turn
4. Check the dashboard for evaluation, best move, and feedback

---

## ✨ What It Does

| Feature | What It Shows |
|---|---|
| **Best Move Arrow** | Green arrow → recommended move |
| **Evaluation Bar** | Gradient bar telling who is winning |
| **Coach Feedback** | "White is better", "Black is winning" etc. |
| **Blunder Alert** | Red alert if you made a big mistake |
| **Check Highlight** | Red glow on king when in check |
| **Last Move Highlight** | Yellow highlight on last played move |
| **Legal Move Dots** | Shows where selected piece can move |
| **Move History** | All moves listed in the sidebar |
| **Engine Info** | Shows Stockfish analysis depth |

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

---

## 📁 Project Files (Simple Explanation)

| File | What It Does |
|---|---|
| `run.py` | **The only file you run.** Starts desktop or web. |
| `server.py` | Web server code (used when you do `python run.py web`) |
| `board_gui.py` | Desktop window code (the board, pieces, sidebar) |
| `engine_handler.py` | Connects to Stockfish engine for analysis |
| `stockfish.exe` | The chess engine (76 MB, included) |
| `config.yaml` | Settings like engine strength, board colors |
| `requirements.txt` | List of Python packages to install |
| `UPDATE.bat` | For publishing updates to GitHub |
| `static/` | Web files (HTML, images) shown in browser mode |

---

## ⚙️ Settings (config.yaml)

```yaml
engine:
  threads: 2          # CPU cores to use (increase = faster)
  hash: 1024          # Memory in MB for analysis
  movetime: 2000      # Analysis time per move (ms)

display:
  dark_square: "#B58863"   # Board dark square color
  light_square: "#F0D9B5"  # Board light square color
```

---

## ❓ Common Problems

**"pip install fails"** → Make sure Python 3.10+ is installed

**"Module not found"** → Run `pip install -r requirements.txt` again

**"Web page not loading"** → Use `http://localhost:8000` not `https`

**"Engine not analyzing"** → Check stockfish.exe exists in the folder

**"Permission denied"** → If on Mac/Linux, run: `chmod +x stockfish`
