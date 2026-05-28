import tkinter as tk
from tkinter import font as tkfont
import sys

# ── constants ────────────────────────────────────────────────────────────────
SIZE = 3
PLAYERS = [
    {"name": "Player X", "mark": "X", "color": "#FF4D6D", "light": "#FF8FA3"},
    {"name": "Player O", "mark": "O", "color": "#4361EE", "light": "#7B9EF9"},
]

BG        = "#0F0F1A"
CELL_BG   = "#1A1A2E"
CELL_HVR  = "#22223B"
GRID_LINE = "#2A2A45"
TEXT_COLOR = "#E8E8F0"
WIN_GLOW  = "#39FF14"
DRAW_CLR  = "#888899"

# ── game logic ────────────────────────────────────────────────────────────────
def create_board():
    return [[" "] * SIZE for _ in range(SIZE)]

def set_cell(board, cell_no, mark):
    r, c = (cell_no - 1) // SIZE, (cell_no - 1) % SIZE
    board[r][c] = mark

def has_mark(board, cell_no):
    r, c = (cell_no - 1) // SIZE, (cell_no - 1) % SIZE
    return board[r][c] != " "

def check_winner(board, mark):
    for row in board:
        if all(c == mark for c in row):
            return [("row", board.index(row))]
    for c in range(SIZE):
        if all(board[r][c] == mark for r in range(SIZE)):
            return [("col", c)]
    if all(board[i][i] == mark for i in range(SIZE)):
        return [("diag", 0)]
    if all(board[i][SIZE - i - 1] == mark for i in range(SIZE)):
        return [("diag", 1)]
    return None

def has_empty_cells(board):
    return any(cell == " " for row in board for cell in row)

def win_cells(win_info):
    """Return list of (row,col) for the winning line."""
    cells = []
    kind, idx = win_info[0]
    if kind == "row":
        cells = [(idx, c) for c in range(SIZE)]
    elif kind == "col":
        cells = [(r, idx) for r in range(SIZE)]
    elif kind == "diag":
        if idx == 0:
            cells = [(i, i) for i in range(SIZE)]
        else:
            cells = [(i, SIZE - i - 1) for i in range(SIZE)]
    return cells

# ── GUI ───────────────────────────────────────────────────────────────────────
class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.board   = create_board()
        self.turn    = 0
        self.winner  = -1
        self.game_over = False
        self.scores  = [0, 0]

        self._build_fonts()
        self._build_ui()
        self._update_status()

    # ── fonts ─────────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.font_title  = tkfont.Font(family="Courier New", size=22, weight="bold")
        self.font_mark   = tkfont.Font(family="Courier New", size=42, weight="bold")
        self.font_status = tkfont.Font(family="Courier New", size=13)
        self.font_score  = tkfont.Font(family="Courier New", size=11)
        self.font_btn    = tkfont.Font(family="Courier New", size=11, weight="bold")

    # ── UI build ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        pad = dict(padx=20, pady=8)

        # title
        tk.Label(self, text="TIC-TAC-TOE", font=self.font_title,
                 bg=BG, fg=TEXT_COLOR).pack(**pad)

        # score bar
        self.score_frame = tk.Frame(self, bg=BG)
        self.score_frame.pack(fill="x", padx=20, pady=(0, 4))
        self.score_labels = []
        for i, p in enumerate(PLAYERS):
            lbl = tk.Label(self.score_frame,
                           text=f"{p['mark']}  0",
                           font=self.font_score,
                           bg=BG, fg=p["color"])
            lbl.pack(side="left" if i == 0 else "right")
            self.score_labels.append(lbl)

        # status label
        self.status_lbl = tk.Label(self, text="", font=self.font_status,
                                   bg=BG, fg=TEXT_COLOR, height=2)
        self.status_lbl.pack()

        # grid
        self.grid_frame = tk.Frame(self, bg=GRID_LINE,
                                   bd=0, relief="flat")
        self.grid_frame.pack(padx=20, pady=4)

        self.buttons = []
        for r in range(SIZE):
            row_btns = []
            for c in range(SIZE):
                cell_no = r * SIZE + c + 1
                btn = tk.Label(
                    self.grid_frame,
                    text="",
                    font=self.font_mark,
                    width=3, height=1,
                    bg=CELL_BG, fg=TEXT_COLOR,
                    relief="flat", cursor="hand2",
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                btn.bind("<Button-1>", lambda e, n=cell_no: self._on_click(n))
                btn.bind("<Enter>",    lambda e, b=btn: self._on_hover(b, True))
                btn.bind("<Leave>",    lambda e, b=btn: self._on_hover(b, False))
                row_btns.append(btn)
            self.buttons.append(row_btns)

        # bottom buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="NEW GAME", font=self.font_btn,
                  bg="#22223B", fg=TEXT_COLOR, activebackground="#2A2A45",
                  activeforeground=TEXT_COLOR, relief="flat", cursor="hand2",
                  padx=14, pady=6, command=self._new_game).pack(side="left", padx=6)

        tk.Button(btn_frame, text="RESET SCORES", font=self.font_btn,
                  bg="#22223B", fg=DRAW_CLR, activebackground="#2A2A45",
                  activeforeground=TEXT_COLOR, relief="flat", cursor="hand2",
                  padx=14, pady=6, command=self._reset_scores).pack(side="left", padx=6)

    # ── hover ──────────────────────────────────────────────────────────────────
    def _on_hover(self, btn, entering):
        if self.game_over or btn["text"]:
            return
        btn.configure(bg=CELL_HVR if entering else CELL_BG)

    # ── click ──────────────────────────────────────────────────────────────────
    def _on_click(self, cell_no):
        if self.game_over:
            return
        if has_mark(self.board, cell_no):
            return

        p = PLAYERS[self.turn]
        set_cell(self.board, cell_no, p["mark"])

        r, c = (cell_no - 1) // SIZE, (cell_no - 1) % SIZE
        btn = self.buttons[r][c]
        btn.configure(text=p["mark"], fg=p["color"], bg=CELL_BG)

        win_info = check_winner(self.board, p["mark"])
        if win_info:
            self.winner = self.turn
            self.game_over = True
            self.scores[self.turn] += 1
            self._highlight_winner(win_info)
            self._update_score_display()
            self._update_status(won=True)
            return

        if not has_empty_cells(self.board):
            self.game_over = True
            self._update_status(draw=True)
            return

        self.turn = (self.turn + 1) % len(PLAYERS)
        self._update_status()

    # ── highlight winner ───────────────────────────────────────────────────────
    def _highlight_winner(self, win_info):
        winning = win_cells(win_info)
        p = PLAYERS[self.winner]
        for (wr, wc) in winning:
            self.buttons[wr][wc].configure(bg=p["color"], fg=BG)
        # dim the rest
        for r in range(SIZE):
            for c in range(SIZE):
                if (r, c) not in winning:
                    self.buttons[r][c].configure(fg=DRAW_CLR)

    # ── status label ───────────────────────────────────────────────────────────
    def _update_status(self, won=False, draw=False):
        if won:
            p = PLAYERS[self.winner]
            self.status_lbl.configure(
                text=f"{p['mark']} wins this round!",
                fg=p["color"])
        elif draw:
            self.status_lbl.configure(text="It's a draw!", fg=DRAW_CLR)
        else:
            p = PLAYERS[self.turn]
            self.status_lbl.configure(
                text=f"{p['mark']}'s turn",
                fg=p["color"])

    # ── score display ──────────────────────────────────────────────────────────
    def _update_score_display(self):
        for i, lbl in enumerate(self.score_labels):
            p = PLAYERS[i]
            lbl.configure(text=f"{p['mark']}  {self.scores[i]}")

    # ── new game / reset ───────────────────────────────────────────────────────
    def _new_game(self):
        self.board     = create_board()
        self.turn      = 0
        self.winner    = -1
        self.game_over = False

        for r in range(SIZE):
            for c in range(SIZE):
                self.buttons[r][c].configure(
                    text="", bg=CELL_BG, fg=TEXT_COLOR)

        self._update_status()

    def _reset_scores(self):
        self.scores = [0, 0]
        self._update_score_display()
        self._new_game()


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()