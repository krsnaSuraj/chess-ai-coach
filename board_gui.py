import sys, math, os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QListWidget, QMessageBox,
                             QFrame, QProgressBar, QPushButton)
from PyQt6.QtGui import (QPainter, QColor, QPen, QFont, QPixmap,
                          QPainterPath, QShortcut, QKeySequence)
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPoint, QPointF, QTimer

import chess
from utils import load_config
from engine_handler import EngineHandler

# === Constants ===
PIECE_IMAGES_DIR = "static/img/chesspieces/wikipedia"
COLORS = {
    "bg": "#0d1117",
    "sidebar": "#161b22",
    "border": "#30363d",
    "accent": "#58a6ff",
    "text": "#f0f6fc",
    "text_dim": "#8b949e",
    "green": "#3fb950",
    "red": "#f85149",
    "yellow": "#d29922",
    "board_light": "#f0d9b5",
    "board_dark": "#b58863",
}

PIECE_MAP = {
    "wP": "wP.png", "wN": "wN.png", "wB": "wB.png",
    "wR": "wR.png", "wQ": "wQ.png", "wK": "wK.png",
    "bP": "bP.png", "bN": "bN.png", "bB": "bB.png",
    "bR": "bR.png", "bQ": "bQ.png", "bK": "bK.png",
}

PIECE_TYPES = {chess.PAWN: "P", chess.KNIGHT: "N", chess.BISHOP: "B",
               chess.ROOK: "R", chess.QUEEN: "Q", chess.KING: "K"}


class ChessBoard(QWidget):
    move_made = pyqtSignal(chess.Move)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.board = chess.Board()
        self.dragged_piece = None
        self.dragged_square = None
        self.drag_start_pos = None
        self.mouse_pos = QPoint()
        self.setMouseTracking(True)
        self.setMinimumSize(360, 360)

        self.flipped = False
        self.drag_cache = None
        self.best_move = None
        self.last_move_squares = []
        self.check_square = None
        self.legal_move_squares = []

        self.light_color = QColor(COLORS["board_light"])
        self.dark_color = QColor(COLORS["board_dark"])
        self.highlight_color = QColor(255, 255, 100, 80)
        self.check_color = QColor(255, 50, 50, 120)
        self.dot_color = QColor(100, 100, 100, 160)
        self.capture_ring_color = QColor(50, 50, 50, 200)
        self.arrow_color = QColor(0, 200, 80, 200)
        self.last_move_color = QColor(255, 255, 100, 90)

        self.raw_pieces = {}
        self.scaled_pieces = {}
        self.current_scale = 0
        self._load_piece_images()

    def _load_piece_images(self):
        for key, filename in PIECE_MAP.items():
            path = os.path.join(PIECE_IMAGES_DIR, filename)
            if os.path.exists(path):
                pix = QPixmap(path)
                if not pix.isNull():
                    self.raw_pieces[key] = pix

    def _get_piece_key(self, piece):
        color = "w" if piece.color == chess.WHITE else "b"
        return color + PIECE_TYPES[piece.piece_type]

    def _scale_pieces(self, square_size):
        if square_size == self.current_scale:
            return
        self.current_scale = square_size
        self.scaled_pieces = {}
        size = int(square_size * 0.88)
        for key, pix in self.raw_pieces.items():
            self.scaled_pieces[key] = pix.scaled(
                size, size, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

    def resizeEvent(self, event):
        self.drag_cache = None
        super().resizeEvent(event)

    def set_board(self, board):
        self.board = board
        self.best_move = None
        self.dragged_piece = None
        self.dragged_square = None
        self.drag_cache = None
        self._update_board_state()
        self.update()

    def _update_board_state(self):
        self.last_move_squares = []
        self.check_square = None
        self.legal_move_squares = []

        if self.board.move_stack:
            last = self.board.peek()
            self.last_move_squares = [last.from_square, last.to_square]

        if self.board.is_check():
            king = self.board.king(self.board.turn)
            if king is not None:
                self.check_square = king

    def set_best_move(self, move):
        self.best_move = move
        self.update()

    def set_flipped(self, flipped):
        self.flipped = flipped
        self.update()

    def set_legal_moves(self, squares):
        self.legal_move_squares = squares
        self.update()

    def _board_coords(self, pos):
        size = min(self.width(), self.height())
        sq = size / 8
        ox = (self.width() - size) / 2
        oy = (self.height() - size) / 2
        x = pos.x() - ox
        y = pos.y() - oy
        if 0 <= x < size and 0 <= y < size:
            col = int(x / sq)
            row = int(y / sq)
            return col, row, sq, ox, oy
        return None, None, sq, ox, oy

    def _to_square(self, col, row):
        if self.flipped:
            return chess.square(7 - col, row)
        return chess.square(col, 7 - row)

    def _to_visual(self, square):
        f = chess.square_file(square)
        r = chess.square_rank(square)
        if self.flipped:
            return 7 - f, r
        return f, 7 - r

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        size = min(self.width(), self.height())
        sq = size / 8
        ox = (self.width() - size) / 2
        oy = (self.height() - size) / 2

        if self.dragged_piece and self.drag_cache:
            painter.drawPixmap(0, 0, self.drag_cache)
            self._draw_dragged_piece(painter, sq)
            return

        self._draw_board_bg(painter, size, ox, oy)
        self._draw_squares(painter, sq, ox, oy)
        self._draw_highlights(painter, sq, ox, oy)
        self._draw_legal_moves(painter, sq, ox, oy)
        self._draw_pieces(painter, sq, ox, oy)
        self._draw_coordinates(painter, sq, ox, oy)
        self._draw_best_move_arrow(painter, sq, ox, oy)

        if self.dragged_piece:
            self._draw_dragged_piece(painter, sq)

    def _draw_board_bg(self, painter, size, ox, oy):
        painter.fillRect(self.rect(), QColor(COLORS["bg"]))
        pen = QPen(QColor(COLORS["border"]), 2)
        painter.setPen(pen)
        rect = QRectF(ox - 1, oy - 1, size + 2, size + 2)
        painter.drawRect(rect)

    def _draw_squares(self, painter, sq, ox, oy):
        for row in range(8):
            for col in range(8):
                f, r = (col, 7 - row) if not self.flipped else (7 - col, row)
                is_light = (f + r) % 2 != 0
                color = self.light_color if is_light else self.dark_color
                rect = QRectF(ox + col * sq, oy + row * sq, sq, sq)

                draw_square = chess.square(f, r)

                if draw_square in self.last_move_squares:
                    c = QColor(self.last_move_color)
                    painter.fillRect(rect, c)
                else:
                    painter.fillRect(rect, color)

    def _draw_highlights(self, painter, sq, ox, oy):
        if self.check_square is not None:
            vcol, vrow = self._to_visual(self.check_square)
            rect = QRectF(ox + vcol * sq, oy + vrow * sq, sq, sq)
            painter.fillRect(rect, self.check_color)

    def _draw_legal_moves(self, painter, sq, ox, oy):
        for square in self.legal_move_squares:
            vcol, vrow = self._to_visual(square)
            cx = ox + vcol * sq + sq / 2
            cy = oy + vrow * sq + sq / 2

            piece = self.board.piece_at(square)
            if piece:
                pen = QPen(self.capture_ring_color, sq * 0.08)
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(QRectF(cx - sq * 0.4, cy - sq * 0.4, sq * 0.8, sq * 0.8))
            else:
                r2 = sq * 0.14
                path = QPainterPath()
                path.addEllipse(QRectF(cx - r2, cy - r2, r2 * 2, r2 * 2))
                painter.fillPath(path, self.dot_color)

    def _draw_pieces(self, painter, sq, ox, oy):
        self._scale_pieces(sq)
        for row in range(8):
            for col in range(8):
                f, r = (col, 7 - row) if not self.flipped else (7 - col, row)
                square = chess.square(f, r)

                if square == self.dragged_square:
                    continue

                piece = self.board.piece_at(square)
                if piece:
                    key = self._get_piece_key(piece)
                    pix = self.scaled_pieces.get(key)
                    if pix:
                        x = ox + col * sq + (sq - pix.width()) / 2
                        y = oy + row * sq + (sq - pix.height()) / 2
                        painter.drawPixmap(int(x), int(y), pix)

    def _draw_dragged_piece(self, painter, sq):
        if not self.dragged_piece:
            return
        self._scale_pieces(sq)
        key = self._get_piece_key(self.dragged_piece)
        pix = self.scaled_pieces.get(key)
        if pix:
            x = self.mouse_pos.x() - pix.width() / 2
            y = self.mouse_pos.y() - pix.height() / 2
            painter.setOpacity(0.85)
            painter.drawPixmap(int(x), int(y), pix)
            painter.setOpacity(1.0)

    def _draw_coordinates(self, painter, sq, ox, oy):
        font = QFont("Segoe UI", int(sq * 0.12))
        font.setWeight(QFont.Weight.Medium)
        painter.setFont(font)

        text_color = QColor(COLORS["text_dim"])
        painter.setPen(text_color)

        for i in range(8):
            if self.flipped:
                file_char = chr(ord('h') - i)
            else:
                file_char = chr(ord('a') + i)

            file_row = 0 if self.flipped else 7
            file_rect = QRectF(ox + i * sq, oy + file_row * sq, sq, sq)
            align = (Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) if self.flipped else \
                    (Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
            painter.drawText(file_rect.adjusted(3, 3, -3, -3), align, file_char)

        for i in range(8):
            rank_num = i + 1 if self.flipped else 8 - i

            rank_col = 7 if self.flipped else 0
            rank_rect = QRectF(ox + rank_col * sq, oy + i * sq, sq, sq)
            align = (Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight) if self.flipped else \
                    (Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            painter.drawText(rank_rect.adjusted(3, 3, -3, -3), align, str(rank_num))

    def _draw_best_move_arrow(self, painter, sq, ox, oy):
        if not self.best_move:
            return

        vcol1, vrow1 = self._to_visual(self.best_move.from_square)
        vcol2, vrow2 = self._to_visual(self.best_move.to_square)

        x1 = ox + vcol1 * sq + sq / 2
        y1 = oy + vrow1 * sq + sq / 2
        x2 = ox + vcol2 * sq + sq / 2
        y2 = oy + vrow2 * sq + sq / 2

        pen = QPen(self.arrow_color, sq * 0.1)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = sq * 0.22

        p1 = QPointF(x2, y2)
        p2 = QPointF(x2 - arrow_size * math.cos(angle - 0.5),
                     y2 - arrow_size * math.sin(angle - 0.5))
        p3 = QPointF(x2 - arrow_size * math.cos(angle + 0.5),
                     y2 - arrow_size * math.sin(angle + 0.5))

        painter.setBrush(self.arrow_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon([p1, p2, p3])

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        pos = event.position()
        col, row, sq, ox, oy = self._board_coords(pos)
        if col is None:
            return

        square = self._to_square(col, row)
        piece = self.board.piece_at(square)

        if piece:
            self.dragged_piece = piece
            self.dragged_square = square
            self.drag_start_pos = pos.toPoint()
            self.mouse_pos = pos.toPoint()
            self.legal_move_squares = [m.to_square for m in self.board.legal_moves
                                       if m.from_square == square]
            self.drag_cache = QPixmap(self.size())
            self.drag_cache.fill(Qt.GlobalColor.transparent)
            tmp = QPainter(self.drag_cache)
            tmp.setRenderHint(QPainter.RenderHint.Antialiasing)
            tmp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self._draw_board_bg(tmp, min(self.width(), self.height()),
                                (self.width() - min(self.width(), self.height())) / 2,
                                (self.height() - min(self.height(), self.height())) / 2)
            size = min(self.width(), self.height())
            sq2 = size / 8
            ox2 = (self.width() - size) / 2
            oy2 = (self.height() - size) / 2
            self._draw_squares(tmp, sq2, ox2, oy2)
            self._draw_highlights(tmp, sq2, ox2, oy2)
            self._draw_pieces(tmp, sq2, ox2, oy2)
            tmp.end()
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragged_piece:
            self.mouse_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if not self.dragged_piece:
            return

        col, row, sq, ox, oy = self._board_coords(event.position())
        self.legal_move_squares = []

        if col is not None:
            target = self._to_square(col, row)
            move = chess.Move(self.dragged_square, target)

            piece = self.board.piece_at(self.dragged_square)
            if piece and piece.piece_type == chess.PAWN:
                rank = chess.square_rank(target)
                if (piece.color == chess.WHITE and rank == 7) or \
                   (piece.color == chess.BLACK and rank == 0):
                    move.promotion = chess.QUEEN

            if move in self.board.legal_moves:
                self.move_made.emit(move)

        self.dragged_piece = None
        self.dragged_square = None
        self.drag_cache = None
        self.drag_start_pos = None
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Coach")
        self.resize(1100, 720)
        self.setStyleSheet(f"background-color: {COLORS['bg']};")

        self.config = load_config()
        self.board = chess.Board()

        from PyQt6.QtWidgets import QInputDialog
        items = ["White", "Black"]
        item, ok = QInputDialog.getItem(self, "Play as",
                                        "Select your color:", items, 0, False)
        self.user_color = chess.WHITE if (ok and item == "White") else chess.BLACK
        self.board_flipped = (self.user_color == chess.BLACK)

        self.engine_handler = EngineHandler(self.config)
        self.engine_handler.analysis_update.connect(self._on_analysis)
        self.engine_handler.error_occurred.connect(self._on_engine_error)
        self.engine_handler.start_engine()

        self.analyzing_fen = None
        self.position_version = 0
        self.analyzing_version_id = None
        self.last_known_move = None
        self.analysis_received = False

        self.redo_stack = []

        self._heartbeat = QTimer()
        self._heartbeat.timeout.connect(self._heartbeat_check)
        self._heartbeat.setInterval(2000)
        self._heartbeat.start()

        self._setup_ui()

        self.run_analysis()
        self._update_feedback()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        self.chess_board = ChessBoard(self.config)
        self.chess_board.set_flipped(self.board_flipped)
        self.chess_board.set_board(self.board)
        self.chess_board.move_made.connect(self._on_move)
        layout.addWidget(self.chess_board, stretch=3)

        sidebar = QFrame()
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['sidebar']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
            QLabel {{
                color: {COLORS['text']};
                background: transparent;
                border: none;
            }}
            QLabel#heading {{
                color: {COLORS['accent']};
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                padding: 8px;
                background-color: {COLORS['bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
            }}
            QLabel#section {{
                color: {COLORS['text_dim']};
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 1.5px;
                padding: 2px 0;
            }}
            QLabel#eval {{
                color: {COLORS['text']};
                font-size: 26px;
                font-weight: bold;
                font-family: 'Segoe UI', monospace;
            }}
            QLabel#bestmove {{
                color: {COLORS['green']};
                font-size: 13px;
                font-family: 'Consolas', monospace;
            }}
            QLabel#feedback {{
                color: {COLORS['text']};
                font-size: 11px;
                padding: 10px;
                background-color: {COLORS['bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                min-height: 50px;
            }}
            QListWidget {{
                background-color: {COLORS['bg']};
                color: {COLORS['text_dim']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 11px;
                font-family: 'Consolas', monospace;
                padding: 2px;
            }}
            QListWidget::item {{
                padding: 2px 6px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            QProgressBar {{
                border: 1px solid {COLORS['border']};
                background-color: {COLORS['bg']};
                border-radius: 3px;
            }}
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 12, 10, 12)
        sidebar_layout.setSpacing(10)

        heading = QLabel("COACH DASHBOARD")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(heading)

        eval_widget = QWidget()
        eval_widget.setStyleSheet("border: none;")
        eval_row = QHBoxLayout(eval_widget)
        eval_row.setContentsMargins(0, 0, 0, 0)
        eval_row.setSpacing(8)

        self.eval_bar = QProgressBar()
        self.eval_bar.setOrientation(Qt.Orientation.Vertical)
        self.eval_bar.setRange(0, 2000)
        self.eval_bar.setValue(1000)
        self.eval_bar.setTextVisible(False)
        self.eval_bar.setFixedWidth(20)
        self.eval_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #30363d;
                background-color: #0d1117;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f85149, stop: 0.4 #3fb950, stop: 0.6 #3fb950, stop: 1 #f85149);
                border-radius: 2px;
            }
        """)
        eval_row.addWidget(self.eval_bar)

        stats = QVBoxLayout()
        stats.setSpacing(2)

        s1 = QLabel("EVALUATION")
        s1.setObjectName("section")
        stats.addWidget(s1)

        self.lbl_eval = QLabel("0.00")
        self.lbl_eval.setObjectName("eval")
        stats.addWidget(self.lbl_eval)

        s2 = QLabel("BEST MOVE")
        s2.setObjectName("section")
        stats.addWidget(s2)

        self.lbl_best = QLabel("-")
        self.lbl_best.setObjectName("bestmove")
        stats.addWidget(self.lbl_best)

        s3 = QLabel("ENGINE")
        s3.setObjectName("section")
        stats.addWidget(s3)

        self.lbl_engine = QLabel("Ready")
        self.lbl_engine.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px;")
        stats.addWidget(self.lbl_engine)

        eval_row.addLayout(stats)
        sidebar_layout.addWidget(eval_widget)

        s4 = QLabel("COACH FEEDBACK")
        s4.setObjectName("section")
        sidebar_layout.addWidget(s4)

        self.lbl_feedback = QLabel("Analyzing position...")
        self.lbl_feedback.setObjectName("feedback")
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.addWidget(self.lbl_feedback, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                border-color: {COLORS['accent']};
                background-color: {COLORS['sidebar']};
            }}
            QPushButton:disabled {{
                color: {COLORS['text_dim']};
                border-color: {COLORS['border']};
            }}
        """)
        self.btn_undo.clicked.connect(self._undo)
        btn_row.addWidget(self.btn_undo)

        self.btn_redo = QPushButton("Redo")
        self.btn_redo.setStyleSheet(self.btn_undo.styleSheet())
        self.btn_redo.clicked.connect(self._redo)
        btn_row.addWidget(self.btn_redo)

        self.btn_new = QPushButton("New Game")
        self.btn_new.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['red']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #d03540;
            }}
        """)
        self.btn_new.clicked.connect(self._new_game)
        btn_row.addWidget(self.btn_new)

        sidebar_layout.addLayout(btn_row)

        s5 = QLabel("MOVE HISTORY")
        s5.setObjectName("section")
        sidebar_layout.addWidget(s5)

        self.move_list = QListWidget()
        sidebar_layout.addWidget(self.move_list, stretch=2)

        layout.addWidget(sidebar, stretch=1)

        QShortcut(QKeySequence("Ctrl+Z"), self).activated.connect(self._undo)
        QShortcut(QKeySequence("Ctrl+Y"), self).activated.connect(self._redo)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self._new_game)

        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['sidebar']};
                color: {COLORS['text_dim']};
                font-size: 10px;
                border-top: 1px solid {COLORS['border']};
            }}
        """)
        self.statusBar().showMessage("Powered by Stockfish 17")

        self.run_analysis()

    def _on_move(self, move):
        try:
            self.prev_eval = getattr(self, 'current_eval', 0.0)

            self.engine_handler.stop_analysis()
            self.chess_board.set_best_move(None)

            if move not in self.board.legal_moves:
                self.chess_board.update()
                return

            san = self.board.san(move)

            self.board.push(move)
            self.position_version += 1
            self.analysis_received = False
            self.last_known_move = None
            self.redo_stack.clear()

            move_num = (len(self.board.move_stack) + 1) // 2
            turn = "W" if self.board.turn == chess.BLACK else "B"
            item_text = f"{move_num}{turn}  {san}"
            self.move_list.addItem(item_text)
            self.move_list.scrollToBottom()
            self._undo_san = (move, item_text)

            self.chess_board.set_board(self.board)
            self._update_feedback()

        except Exception as e:
            print(f"Move error: {e}")

    def _undo(self):
        if not self.board.move_stack:
            return
        try:
            self.engine_handler.stop_analysis()
            item = self.move_list.takeItem(self.move_list.count() - 1)
            item_text = item.text() if item else ""
            move = self.board.pop()
            self.redo_stack.append((move, item_text))
            self.position_version += 1
            self.analysis_received = False
            self.last_known_move = None

            self.chess_board.set_board(self.board)
            self._update_feedback()
        except Exception as e:
            print(f"Undo error: {e}")

    def _new_game(self):
        try:
            from PyQt6.QtWidgets import QInputDialog
            items = ["White", "Black"]
            item, ok = QInputDialog.getItem(self, "Play as",
                                            "Select your color:", items, 0, False)
            if not ok:
                return
            self.user_color = chess.WHITE if item == "White" else chess.BLACK
            self.board_flipped = (self.user_color == chess.BLACK)

            self.engine_handler.stop_analysis()
            self.board.reset()
            self.redo_stack.clear()
            self.position_version += 1
            self.analysis_received = False
            self.last_known_move = None
            self.current_eval = 0.0
            self.prev_eval = 0.0
            self.move_list.clear()
            self.lbl_eval.setText("0.00")
            self.lbl_best.setText("-")
            self.lbl_feedback.setText("New game started")
            self.lbl_feedback.setStyleSheet(
                f"color: {COLORS['text']}; padding: 10px;"
                f"background: {COLORS['bg']};"
                f"border: 1px solid {COLORS['border']}; border-radius: 4px;"
            )
            self.lbl_engine.setText("Ready")
            self.eval_bar.setValue(1000)
            self.chess_board.set_flipped(self.board_flipped)
            self.chess_board.set_board(self.board)
            self._update_feedback()
        except Exception as e:
            print(f"New game error: {e}")

    def _redo(self):
        if not self.redo_stack:
            return
        try:
            self.engine_handler.stop_analysis()
            move, san = self.redo_stack.pop()
            self.board.push(move)
            self.position_version += 1
            self.analysis_received = False
            self.last_known_move = None

            move_num = (len(self.board.move_stack) + 1) // 2
            turn = "W" if self.board.turn == chess.BLACK else "B"
            self.move_list.addItem(f"{move_num}{turn}  {san}")
            self.move_list.scrollToBottom()

            self.chess_board.set_board(self.board)
            self._update_feedback()
        except Exception as e:
            print(f"Redo error: {e}")

    def run_analysis(self):
        self.analyzing_fen = self.board.fen()
        self.analyzing_version_id = self.position_version
        self.engine_handler.start_analysis(self.board.copy())

    def _on_analysis(self, info):
        try:
            if self.analyzing_version_id != self.position_version:
                return
            if self.analyzing_fen and self.analyzing_fen != self.board.fen():
                return

            score = info.get("score")
            if not score:
                return

            if score.is_mate():
                mate = score.relative.mate() or 0
                text = f"M{mate}"
                val = 1000 if mate > 0 else -1000
                cur_eval = float('inf') if mate > 0 else float('-inf')
            else:
                cp = score.relative.score(mate_score=10000)
                if self.board.turn == chess.BLACK:
                    cp = -cp
                text = f"{cp / 100:.2f}"
                val = max(-1000, min(1000, cp))
                cur_eval = cp / 100.0

            self.current_eval = cur_eval

            depth = info.get("depth", 0)
            self.lbl_engine.setText(f"Depth {depth}")
            self.lbl_eval.setText(text)

            bar_val = val + 1000
            self.eval_bar.setValue(int(bar_val))

            if not self.can_show_coach():
                self.chess_board.set_best_move(None)
                return

            if score.is_mate():
                self.engine_handler.stop_analysis()
                pv = info.get("pv")
                if pv:
                    self.last_known_move = pv[0]
                    self.chess_board.set_best_move(pv[0])
                    self.lbl_best.setText(pv[0].uci())
                    self.lbl_feedback.setText(f"CHECKMATE IN {abs(mate)}!")
                    self.lbl_feedback.setStyleSheet(
                        f"color: {COLORS['green']}; padding: 10px;"
                        f"border: 1px solid {COLORS['green']}; border-radius: 4px;"
                    )
                    self.analysis_received = True
                return

            feedback = "Balanced"
            if val > 100:
                feedback = "White is better"
            if val > 300:
                feedback = "White is winning"
            if val < -100:
                feedback = "Black is better"
            if val < -300:
                feedback = "Black is winning"

            prev = getattr(self, 'prev_eval', None)
            if prev is not None and not score.is_mate():
                delta = cur_eval - prev
                if (self.user_color == chess.WHITE and delta < -1.0) or \
                   (self.user_color == chess.BLACK and delta > 1.0):
                    feedback = "BLUNDER!\nOpponent missed a chance."
                    self.lbl_feedback.setStyleSheet(
                        f"color: {COLORS['red']}; padding: 10px;"
                        f"border: 1px solid {COLORS['red']}; border-radius: 4px;"
                    )
                else:
                    self.lbl_feedback.setStyleSheet(
                        f"color: {COLORS['text']}; padding: 10px;"
                        f"background: {COLORS['bg']};"
                        f"border: 1px solid {COLORS['border']}; border-radius: 4px;"
                    )

            self.lbl_feedback.setText(feedback)

            pv = info.get("pv")
            if pv:
                self.last_known_move = pv[0]
                self.chess_board.set_best_move(pv[0])
                self.lbl_best.setText(pv[0].uci())
                self.analysis_received = True

        except Exception as e:
            print(f"Analysis error: {e}")

    def can_show_coach(self):
        return self.board.turn == self.user_color

    def _update_feedback(self):
        if self.can_show_coach() and not self.board.is_game_over():
            self.run_analysis()
        else:
            self.last_known_move = None
            self.chess_board.set_best_move(None)
            self.lbl_best.setText("-")
            self.lbl_feedback.setText("Waiting for your turn...")
            self.lbl_feedback.setStyleSheet(
                f"color: {COLORS['text']}; padding: 10px;"
                f"background: {COLORS['bg']};"
                f"border: 1px solid {COLORS['border']}; border-radius: 4px;"
            )

    def _heartbeat_check(self):
        if not self.can_show_coach():
            return
        if self.analysis_received:
            self.analysis_received = False
            return
        if self.last_known_move:
            self.chess_board.set_best_move(self.last_known_move)
            self.lbl_best.setText(f"{self.last_known_move.uci()} (cached)")

    def _on_engine_error(self, msg):
        QMessageBox.warning(self, "Engine Error", msg)

    def closeEvent(self, event):
        self.engine_handler.stop_engine()
        event.accept()
