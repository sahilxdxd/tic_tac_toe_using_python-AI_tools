import tkinter as tk
from tkinter import messagebox, simpledialog
import math, random

# -----------------------------
# Minimax + Alpha-Beta
# -----------------------------
def evaluate(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return 10 if board[i][0] == "O" else -10
        if board[0][i] == board[1][i] == board[2][i] != "":
            return 10 if board[0][i] == "O" else -10
    if board[0][0] == board[1][1] == board[2][2] != "":
        return 10 if board[0][0] == "O" else -10
    if board[0][2] == board[1][1] == board[2][0] != "":
        return 10 if board[0][2] == "O" else -10
    return 0

def is_moves_left(board):
    return any("" in row for row in board)

def minimax(board, depth, isMax, alpha, beta, depth_limit):
    score = evaluate(board)
    if score == 10 or score == -10:
        return score - depth if score == 10 else score + depth
    if not is_moves_left(board) or depth >= depth_limit:
        return 0

    if isMax:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    val = minimax(board, depth + 1, False, alpha, beta, depth_limit)
                    board[i][j] = ""
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    val = minimax(board, depth + 1, True, alpha, beta, depth_limit)
                    board[i][j] = ""
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(board, difficulty):
    best_val = -math.inf
    best_move = (-1, -1)
    depth_limit = {"Easy": 1, "Medium": 3, "Hard": 9}[difficulty]

    # For easy difficulty, make random move sometimes
    if difficulty == "Easy" and random.random() < 0.5:
        available = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        return random.choice(available)

    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                move_val = minimax(board, 0, False, -math.inf, math.inf, depth_limit)
                board[i][j] = ""
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# -----------------------------
# GUI Class
# -----------------------------
class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI - Minimax + Alpha-Beta")
        self.root.resizable(False, False)

        self.username = simpledialog.askstring("Player Name", "Enter your name:", parent=root)
        if not self.username:
            self.username = "Player"

        self.user_wins = 0
        self.ai_wins = 0

        self.board = [[""] * 3 for _ in range(3)]
        self.buttons = [[None] * 3 for _ in range(3)]

        self.difficulty = tk.StringVar(value="Hard")

        self.status_label = tk.Label(root, text=f"{self.username}'s Turn (X)", font=("Arial", 16))
        self.status_label.pack(pady=8)

        # Difficulty dropdown
        diff_frame = tk.Frame(root)
        diff_frame.pack()
        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(diff_frame, self.difficulty, "Easy", "Medium", "Hard").pack(side=tk.LEFT)

        # Board Frame
        self.board_frame = tk.Frame(root, bg="black")
        self.board_frame.pack(pady=10)

        # Fixed-size grid buttons
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame, text="", font=("Arial", 32, "bold"),
                    width=3, height=1,  # fixed character units
                    bg="white", relief="solid", bd=2,
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.grid(row=i, column=j, padx=3, pady=3, ipadx=20, ipady=20)
                self.buttons[i][j] = btn

        # Scoreboard
        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 13))
        self.score_label.pack(pady=5)

        # Restart Button
        tk.Button(root, text="Restart Game", font=("Arial", 12, "bold"),
                  bg="#0078D7", fg="white", width=15, command=self.reset_board).pack(pady=8)

    def get_score_text(self):
        return f"🏆 {self.username}: {self.user_wins}   🤖 AI: {self.ai_wins}"

    def player_move(self, i, j):
        if self.board[i][j] == "" and evaluate(self.board) == 0:
            self.board[i][j] = "X"
            self.buttons[i][j].config(text="X", fg="red", state="disabled")
            if self.check_winner():
                return
            self.status_label.config(text="AI's Turn (O)")
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if not is_moves_left(self.board):
            return
        move = find_best_move(self.board, self.difficulty.get())
        if move != (-1, -1):
            i, j = move
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="O", fg="blue", state="disabled")
        self.check_winner()
        self.status_label.config(text=f"{self.username}'s Turn (X)")

    def check_winner(self):
        score = evaluate(self.board)
        if score == 10:
            self.ai_wins += 1
            self.status_label.config(text="AI Wins 😎", fg="blue")
            self.disable_all()
            messagebox.showinfo("Result", "AI Wins 😎")
            self.score_label.config(text=self.get_score_text())
            return True
        elif score == -10:
            self.user_wins += 1
            self.status_label.config(text=f"{self.username} Wins 🎉", fg="red")
            self.disable_all()
            messagebox.showinfo("Result", f"{self.username} Wins 🎉")
            self.score_label.config(text=self.get_score_text())
            return True
        elif not is_moves_left(self.board):
            self.status_label.config(text="Draw 🤝", fg="black")
            messagebox.showinfo("Result", "It's a Draw 🤝")
            return True
        return False

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_board(self):
        self.board = [[""] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", fg="black", bg="white")
        self.status_label.config(text=f"{self.username}'s Turn (X)", fg="black")

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeAI(root)
    root.mainloop()
