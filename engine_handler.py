import chess
import chess.engine
from PyQt6.QtCore import QThread, pyqtSignal, QObject
import subprocess
import os


class EngineHandler(QObject):
    analysis_update = pyqtSignal(dict)
    best_move_found = pyqtSignal(chess.Move)
    error_occurred = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.engine_path = config.get("engine", {}).get("path", "stockfish.exe")
        self.engine = None
        self.analysis_thread = None
        self.pending_board = None

    def start_engine(self):
        try:
            if not os.path.exists(self.engine_path):
                if os.path.exists(os.path.join(os.getcwd(), self.engine_path)):
                    self.engine_path = os.path.join(os.getcwd(), self.engine_path)
                else:
                    raise FileNotFoundError(f"Stockfish executable not found at {self.engine_path}")

            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            self.engine = chess.engine.SimpleEngine.popen_uci(
                self.engine_path,
                startupinfo=startupinfo
            )

            self.engine.configure({"Hash": self.config.get("engine", {}).get("hash", 16)})
            self.engine.configure({"Threads": self.config.get("engine", {}).get("threads", 1)})
            print("Stockfish engine started successfully.")

        except Exception as e:
            self.error_occurred.emit(str(e))
            print(f"Failed to start engine: {e}")

    def stop_engine(self):
        self._stop_current_thread_async()
        if self.engine:
            self.engine.quit()
            self.engine = None

    def start_analysis(self, board):
        val_snapshot = board.copy()
        self.pending_board = val_snapshot

        if self.analysis_thread and self.analysis_thread.isRunning():
            self._stop_current_thread_async()
            return

        self._launch_thread(val_snapshot)

    def stop_analysis(self):
        self.pending_board = None
        self._stop_current_thread_async()

    def _stop_current_thread_async(self):
        if self.analysis_thread:
            try:
                self.analysis_thread.info_received.disconnect()
            except Exception:
                pass

            self.analysis_thread.stop()

    def _launch_thread(self, board):
        if not self.engine:
            return

        self.analysis_thread = AnalysisThread(self.engine, board, self.config)
        self.analysis_thread.info_received.connect(self.analysis_update.emit)
        self.analysis_thread.finished.connect(self._on_thread_finished)
        self.analysis_thread.start()

    def _on_thread_finished(self):
        if self.pending_board:
            next_board = self.pending_board
            self.pending_board = None
            self._launch_thread(next_board)

    def get_emergency_move(self, board):
        if not self.engine:
            return None
        try:
            result = self.engine.play(board, chess.engine.Limit(time=0.05))
            return result.move
        except Exception as e:
            print(f"Emergency analysis failed: {e}")
            return None


class AnalysisThread(QThread):
    info_received = pyqtSignal(dict)

    def __init__(self, engine, board, config):
        super().__init__()
        self.engine = engine
        self.board = board
        self.config = config
        self.is_running = True

    def run(self):
        try:
            with self.engine.analysis(self.board) as analysis:
                for info in analysis:
                    if not self.is_running:
                        break
                    self.info_received.emit(info)
        except Exception as e:
            print(f"Analysis thread error: {e}")

    def stop(self):
        self.is_running = False
