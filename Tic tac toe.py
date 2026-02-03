import tkinter as tk
from tkinter import messagebox
import math



BG_COLOR = "#0b0f1a"       
GRID_COLOR = "#1f2a44"
X_COLOR = "#00e5ff"       
O_COLOR = "#ff4dd2"       
BTN_COLOR = "#11162a"
TEXT_COLOR = "#e6f1ff"

WINDOW_SIZE = 420
CELL_SIZE = 120
PADDING = 30

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.mode = tk.StringVar(value="AI")  
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.create_ui()

    def create_ui(self):
        
        top = tk.Frame(self.root, bg=BG_COLOR)
        top.pack(pady=10)

        tk.Label(top, text="GAME MODE", fg=TEXT_COLOR, bg=BG_COLOR,
                 font=("Orbitron", 10, "bold")).pack(side=tk.LEFT, padx=8)

        tk.Radiobutton(top, text="VS AI", variable=self.mode, value="AI",
                       fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR,
                       activebackground=BG_COLOR, activeforeground=TEXT_COLOR).pack(side=tk.LEFT)

        tk.Radiobutton(top, text="2 PLAYERS", variable=self.mode, value="PVP",
                       fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR,
                       activebackground=BG_COLOR, activeforeground=TEXT_COLOR).pack(side=tk.LEFT)

        tk.Button(top, text="RESET", command=self.reset,
                  bg=BTN_COLOR, fg=TEXT_COLOR, relief="flat").pack(side=tk.LEFT, padx=12)

        
        self.canvas = tk.Canvas(self.root, width=WINDOW_SIZE, height=WINDOW_SIZE,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(1, 3):
            # vertical
            self.canvas.create_line(PADDING + i * CELL_SIZE, PADDING,
                                    PADDING + i * CELL_SIZE, PADDING + 3 * CELL_SIZE,
                                    fill=GRID_COLOR, width=3, tags="grid")
            # horizontal
            self.canvas.create_line(PADDING, PADDING + i * CELL_SIZE,
                                    PADDING + 3 * CELL_SIZE, PADDING + i * CELL_SIZE,
                                    fill=GRID_COLOR, width=3, tags="grid")

    def handle_click(self, event):
        row, col = self.get_cell(event.x, event.y)
        if row is None:
            return
        if self.board[row][col] == "":
            self.make_move(row, col, self.current_player)
            if self.check_game_over():
                return

            if self.mode.get() == "AI" and self.current_player == "O":
                self.root.after(300, self.ai_move)

    def get_cell(self, x, y):
        if not (PADDING <= x <= PADDING + 3 * CELL_SIZE and
                PADDING <= y <= PADDING + 3 * CELL_SIZE):
            return None, None
        col = (x - PADDING) // CELL_SIZE
        row = (y - PADDING) // CELL_SIZE
        return int(row), int(col)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.draw_symbol(row, col, player)
        self.current_player = "O" if player == "X" else "X"

    def draw_symbol(self, row, col, player):
        cx = PADDING + col * CELL_SIZE + CELL_SIZE // 2
        cy = PADDING + row * CELL_SIZE + CELL_SIZE // 2

        if player == "X":
            self.canvas.create_line(cx - 30, cy - 30, cx + 30, cy + 30,
                                    fill=X_COLOR, width=4)
            self.canvas.create_line(cx + 30, cy - 30, cx - 30, cy + 30,
                                    fill=X_COLOR, width=4)
        else:
            self.canvas.create_oval(cx - 32, cy - 32, cx + 32, cy + 32,
                                    outline=O_COLOR, width=4)

   

    def check_winner(self):
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != "" and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} Wins! 🎉")
            self.reset()
            return True
        elif all(self.board[r][c] != "" for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "🤝 It's a Draw!")
            self.reset()
            return True
        return False

 
    def ai_move(self):
        best_score = -math.inf
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    score = self.minimax(False)
                    self.board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            self.make_move(best_move[0], best_move[1], "O")
            self.check_game_over()

    def minimax(self, is_maximizing):
        winner = self.check_winner()
        if winner == "O":
            return 1
        if winner == "X":
            return -1
        if all(self.board[r][c] != "" for r in range(3) for c in range(3)):
            return 0

        if is_maximizing:
            best = -math.inf
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == "":
                        self.board[r][c] = "O"
                        best = max(best, self.minimax(False))
                        self.board[r][c] = ""
            return best
        else:
            best = math.inf
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == "":
                        self.board[r][c] = "X"
                        best = min(best, self.minimax(True))
                        self.board[r][c] = ""
            return best

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.canvas.delete("all")
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()