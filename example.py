import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Frame, Button, messagebox
import os

# Constants
FPS = 60
HEIGHT = 800
WIDTH = 800
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS
WHITE = "white"
BLACK = "black"
BLUE = "blue"

# Help message function
def help():
    help_text = '''\n● Checkers is a two-player game played on an 8x8 board.
\n● Pieces move only on dark squares. Red moves first.
\n● The goal is to capture all of the opponent's pieces or block them.
\n● Moves are recorded, e.g., if Red moves from 9 to 13, it's recorded as 9-13.'''
    messagebox.showinfo("Help", help_text)

# Piece class
class Piece:
    def __init__(self, color, row, col, king=False):
        self.color = color
        self.row = row
        self.col = col
        self.king = king

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col

# Board class
class Board(tk.Frame):
    def __init__(self, parent, length, width, background_color, border_thickness, border_color):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.length = length
        self.width = width
        self.background_color = background_color
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.config(height=length * SQUARE_SIZE, width=width * SQUARE_SIZE, bg=self.background_color, highlightthickness=self.border_thickness, highlightbackground=self.border_color)
        self.pack(side=tk.BOTTOM)
        self.board = []
        self.square_color = None
        self.squares = {}
        self.ranks = "abcdefgh"
        self.white_image = None
        self.black_image = None
        self.set_squares()
        self.load_piece_images()
        self.place_pieces()

    def set_squares(self):
        for x in range(ROWS):
            for y in range(COLS):
                if (x + y) % 2 == 0:
                    self.square_color = "tan4"
                else:
                    self.square_color = "burlywood1"

                label = tk.Label(self, bg=self.square_color, width=10, height=5)
                label.grid(row=8 - x, column=y)
                pos = self.ranks[y] + str(x + 1)
                self.squares.setdefault(pos, label)

    from PIL import ImageTk

    def load_piece_images(self):
        # Load white and black piece images
        white_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "white_piece.png")
        black_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "black_piece.png")
        self.white_image = Image.open(white_piece_image_path)
        self.black_image = Image.open(black_piece_image_path)

    def place_pieces(self):
        for x in range(8):
            self.board.append([])
            for y in range(8):
                pos = self.ranks[y] + str(x + 1)
                if (x + y) % 2 != 0:
                    if 0 <= x < 3: 
                        piece = ImageTk.PhotoImage(self.black_image)
                        self.squares[pos].config(image=piece, width=80, height=80)
                        self.squares[pos].image = piece
                        self.board[x].append(Piece("black", x, y))
                    elif 5 <= x < 8:  # Place white pieces
                        piece = ImageTk.PhotoImage(self.white_image)
                        self.squares[pos].config(image=piece, width=80, height=80)
                        self.squares[pos].image = piece
                        self.board[x].append(Piece("white", x, y))
                    else:
                        self.squares[pos].config(width=11, height=5) 
                else:
                    self.squares[pos].config(width=11, height=5) 
    def move_piece(self, piece, row, col):
        if piece:
            self.board[piece.row][piece.col], self.board[row][col] = None, piece
            piece.move(row, col)
            old_pos = self.ranks[piece.col] + str(ROWS - piece.row)
            new_pos = self.ranks[col] + str(ROWS - row)
            self.squares[old_pos].config(image='')
            if piece.color == "white":
                self.squares[new_pos].config(image=self.white_image)
            else:
                self.squares[new_pos].config(image=self.black_image)
            if row == 0 or row == ROWS - 1:
                piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

# Game class
class Game:
    def __init__(self, root):
        self._init()
        self.root = root
        self.board = Board(root, 8, 8, "light grey", 5, "black")
        self.root.bind("<Button-1>", self.on_click)

    def update(self):
        self.board.place_pieces()

    def _init(self):
        self.selected = None
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return None

    def reset(self):
        self._init()
        self.update()

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            self.update()
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and not piece and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)
            self.change_turn()
        else:
            return False
        return True

    def get_valid_moves(self, piece):
        return [(piece.row + 1, piece.col + 1), (piece.row + 1, piece.col - 1)]

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            self.board.squares[self.board.ranks[col] + str(ROWS - row)].config(bg=BLUE)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def on_click(self, event):
        pos = (event.x, event.y)
        row, col = self.get_row_col_from_mouse(pos)
        if not self.selected:
            self.select(row, col)
        else:
            if not self._move(row, col):
                self.selected = None
        self.update()

# Main function
def main():
    root = tk.Tk()
    root.title("Checkers Game")

    top_frame = Frame(root)
    top_frame.pack(side=tk.TOP)

    def restart_game():
        game.reset()

    restart_button = Button(top_frame, fg="blue", text="Restart", command=restart_game)
    restart_button.pack(side=tk.LEFT)

    help_button = Button(top_frame, fg="blue", text="Help", command=help)
    help_button.pack(side=tk.LEFT)

    exit_button = Button(top_frame, fg="red", text="Exit", command=root.quit)
    exit_button.pack(side=tk.RIGHT)

    game = Game(root)

    def game_loop():
        if game.winner() is not None:
            print(game.winner())
            root.quit()
        game.update()
        root.after(1000 // FPS, game_loop)

    root.after(1000 // FPS, game_loop)
    root.mainloop()

main()
