import tkinter as tk
from Checkers.sourceCode import Board

HEIGHT = 8000
WIDTH = 8000
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

BLACK = "black"
WHITE = "white"
BLUE = "blue"

class Game:
    def __init__(self, root):
        self._init()
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def update(self):
        self.draw_board()
        self.draw_valid_moves(self.valid_moves)

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()
        self.update()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            self.update()
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            self.canvas.create_oval(col * SQUARE_SIZE + SQUARE_SIZE//2 - 15, row * SQUARE_SIZE + SQUARE_SIZE//2 - 15,
                                    col * SQUARE_SIZE + SQUARE_SIZE//2 + 15, row * SQUARE_SIZE + SQUARE_SIZE//2 + 15,
                                    fill=BLUE)

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
        self.select(row, col)
        self.update()


