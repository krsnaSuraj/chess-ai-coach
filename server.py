import chess
import chess.engine
import yaml
import os
import threading
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


class GamePhase(Enum):
    AWAITING_COLOR = "awaiting_color"
    PLAYING = "playing"
    GAME_OVER = "game_over"


class GameController:
    def __init__(self):
        self.board = chess.Board()
        self.human_side = None
        self.game_phase = GamePhase.AWAITING_COLOR
        self.move_number = 1
        self.lock = threading.Lock()

    def start_game(self, human_is_white: bool):
        with self.lock:
            self.board.reset()
            self.human_side = chess.WHITE if human_is_white else chess.BLACK
            self.move_number = 1
            self.game_phase = GamePhase.PLAYING

    def record_move(self, move: chess.Move):
        self.board.push(move)
        if self.board.turn == chess.WHITE:
            self.move_number += 1
        if self.board.is_game_over():
            self.game_phase = GamePhase.GAME_OVER


game_controller = GameController()

CONFIG_PATH = "config.yaml"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

ENGINE_PATH = config.get("engine", {}).get("path", "stockfish.exe")
MOVETIME = config.get("engine", {}).get("movetime", 2000) / 1000.0

engine = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UnifiedResponse(BaseModel):
    ok: bool
    mode: str
    fen: str
    move: str | None = None
    coach: dict | None = None
    error: str | None = None


class StartGameRequest(BaseModel):
    human_is_white: bool


class HumanMoveRequest(BaseModel):
    move_uci: str


def get_engine():
    global engine
    if engine is None:
        try:
            engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
        except Exception as e:
            print(f"Failed to start engine: {e}")
            return None
    return engine


@app.on_event("shutdown")
def shutdown():
    global engine
    if engine:
        engine.quit()
        engine = None


@app.get("/api/health")
def health_check():
    eng = get_engine()
    return {"status": "ok", "engine_running": eng is not None}


@app.post("/api/start_game")
def start_game(request: StartGameRequest):
    try:
        game_controller.start_game(request.human_is_white)
        return _build_response()
    except Exception as e:
        return _error_response(str(e))


@app.get("/api/game_state")
def get_game_state():
    try:
        return _build_response()
    except Exception as e:
        return _error_response(str(e))


@app.post("/api/human_move")
def human_move(request: HumanMoveRequest):
    try:
        if game_controller.game_phase != GamePhase.PLAYING:
            return _error_response("Game not in progress")

        try:
            move = chess.Move.from_uci(request.move_uci)
            if move not in game_controller.board.legal_moves:
                return _error_response("Illegal move")
        except Exception:
            return _error_response("Invalid move format")

        with game_controller.lock:
            game_controller.record_move(move)

        return _build_response()
    except Exception as e:
        return _error_response(str(e))


def _build_response() -> UnifiedResponse:
    mode = "idle"
    if game_controller.game_phase == GamePhase.PLAYING:
        mode = "coach"
    elif game_controller.game_phase == GamePhase.GAME_OVER:
        mode = "idle"

    coach_data = None
    if mode == "coach":
        if game_controller.board.turn == game_controller.human_side:
            coach_data = _run_coach_analysis_safe()

    return UnifiedResponse(
        ok=True,
        mode=mode,
        fen=game_controller.board.fen(),
        move=None,
        coach=coach_data,
        error=None
    )


def _error_response(msg: str) -> UnifiedResponse:
    return UnifiedResponse(
        ok=False,
        mode="idle",
        fen=game_controller.board.fen(),
        error=msg
    )


def _run_coach_analysis_safe() -> dict | None:
    eng = get_engine()
    if eng is None:
        return None
    try:
        info = eng.analyse(game_controller.board, chess.engine.Limit(time=MOVETIME))
        score = info.get("score")
        cp = score.white().score(mate_score=10000)
        mate = score.white().mate()
        depth = info.get("depth", 0)

        if mate is not None:
            eval_text = f"M{abs(mate)}"
            if mate > 0:
                eval_text = "+" + eval_text
            else:
                eval_text = "-" + eval_text
        else:
            eval_text = f"{cp / 100:.2f}"
            if cp > 0:
                eval_text = "+" + eval_text

        pv = info.get("pv", [])
        best_move = pv[0].uci() if pv else None

        return {
            "best_move": best_move,
            "eval": eval_text,
            "pv": " ".join([m.uci() for m in pv]),
            "thinking": [f"Depth {depth}: {eval_text}"]
        }
    except Exception as e:
        print(f"Coach error: {e}")
        return None


app.mount("/", StaticFiles(directory="static", html=True), name="static")
