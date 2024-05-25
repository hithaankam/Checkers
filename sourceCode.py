import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Frame, Button, messagebox

# Checkers game logic
class Checkers:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 'r'
        self.directions = {
            'r': [(1, -1), (1, 1)],
            'b': [(-1, -1), (-1, 1)],
            'R': [(1, -1), (1, 1), (-1, -1), (-1, 1)],
            'B': [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        }

    def initialize_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    board[i][j] = 'r'
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    board[i][j] = 'b'
        return board

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def has_piece(self, position):
        x, y = position
        return self.board[x][y] != ' ' and self.board[x][y].lower() == self.current_turn

    def is_valid_move(self, start, end):
        sx, sy = start
        ex, ey = end

        if not (0 <= ex < 8 and 0 <= ey < 8):
            return False
        if self.board[ex][ey] != ' ':
            return False
        if self.board[sx][sy].lower() != self.current_turn:
            return False

        piece = self.board[sx][sy]
        valid_directions = self.directions[piece]

        for direction in valid_directions:
            if (ex, ey) == (sx + direction[0], sy + direction[1]):
                return True

        # Check for captures
        for direction in valid_directions:
            mid_x, mid_y = sx + direction[0], sy + direction[1]
            end_x, end_y = sx + 2 * direction[0], sy + 2 * direction[1]
            if (end_x, end_y) == (ex, ey):
                if 0 <= mid_x < 8 and 0 <= mid_y < 8:
                    if self.board[mid_x][mid_y] != ' ' and self.board[mid_x][mid_y].lower() != self.current_turn:
                        return True

        return False

    def get_valid_moves(self, start):
        sx, sy = start
        valid_moves = []

        piece = self.board[sx][sy]
        valid_directions = self.directions[piece]

        for direction in valid_directions:
            ex, ey = sx + direction[0], sy + direction[1]
            if 0 <= ex < 8 and 0 <= ey < 8 and self.is_valid_move(start, (ex, ey)):
                valid_moves.append((ex, ey))

            # Check for captures
            ex, ey = sx + 2 * direction[0], sy + 2 * direction[1]
            if 0 <= ex < 8 and 0 <= ey < 8 and self.is_valid_move(start, (ex, ey)):
                valid_moves.append((ex, ey))

        return valid_moves

    def move_piece(self, start, end):
        if not self.has_piece(start):
            messagebox.showerror("Invalid Move", "No piece at the starting position or not your piece")
            return False

        if not self.is_valid_move(start, end):
            messagebox.showerror("Invalid Move", "Invalid move")
            return False

        sx, sy = start
        ex, ey = end

        if abs(ex - sx) == 2 and abs(ey - sy) == 2:
            mid_x, mid_y = (sx + ex) // 2, (sy + ey) // 2
            self.board[mid_x][mid_y] = ' '

        self.board[ex][ey] = self.board[sx][sy]
        self.board[sx][sy] = ' '

        self.check_king(ex, ey)

        self.current_turn = 'b' if self.current_turn == 'r' else 'r'
        return True

    def check_king(self, x, y):
        if self.board[x][y] == 'r' and x == 7:
            self.board[x][y] = 'R'
        elif self.board[x][y] == 'b' and x == 0:
            self.board[x][y] = 'B'

# GUI for the Checkers game
def help():
    help_text = '''\n● Checkers is a two-player game played on an 8x8 grid with a dark square in each player's lower left corner.
\n● Pieces move only on dark squares which are numbered. Numbers are used to record the
moves, for example, if Red moves from square 9 to square 13, then it is recorded as:
9-13.
\n● Each player controls its own army of pieces (men). The player who controls Red pieces
moves first. The pieces (also known as 'men') are arranged as shown on the left.
\n● The goal in the checkers game is either to capture all of the opponent's pieces or to
blockade them. If neither player can accomplish the above, the game is a draw.'''
    messagebox.showinfo("Help", help_text)

class Board(tk.Frame):
    def __init__(self, parent, game, length, width, background_color, border_thickness, border_color):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.game = game
        self.length = length
        self.width = width
        self.background_color = background_color
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.config(height=1000*self.length, width=1000*self.width, bg=self.background_color, highlightthickness=self.border_thickness, highlightbackground=self.border_color)
        self.pack(side=tk.BOTTOM)
        
        self.square_color = None
        self.squares = {}
        self.ranks = "abcdefgh"
        self.white_image = None
        self.black_image = None
        self.white_king_image = None
        self.black_king_image = None
        self.set_squares()

        self.selected_piece = None
        self.valid_moves = []
        self.load_piece_images()
        self.place_pieces()

    def set_squares(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    self.square_color = "tan4"
                else:
                    self.square_color = "burlywood1"

                B = tk.Button(self, bg=self.square_color, activebackground="lawn green", command=lambda x=x, y=y: self.select_square(x, y))
                B.grid(row=8 - x, column=y)
                pos = self.ranks[y] + str(x + 1)
                self.squares.setdefault(pos, B)
    
    def load_piece_images(self):
        self.white_image = Image.open(r"D:\Hitha\Checkers\Checkers\white_piece.png")  # Ensure the path is correct
        self.black_image = Image.open(r"D:\Hitha\Checkers\Checkers\black_piece.png")  # Ensure the path is correct
        self.white_king_image = Image.open(r"D:\Hitha\Checkers\Checkers\crown.png")  # Ensure the path is correct
        self.black_king_image = Image.open(r"D:\Hitha\Checkers\Checkers\crown.png")  # Ensure the path is correct

        self.white_image = self.white_image.resize((80, 80), Image.LANCZOS)
        self.black_image = self.black_image.resize((80, 80), Image.LANCZOS)
        self.white_king_image = self.white_king_image.resize((80, 80), Image.LANCZOS)
        self.black_king_image = self.black_king_image.resize((80, 80), Image.LANCZOS)

        self.white_image = ImageTk.PhotoImage(self.white_image)
        self.black_image = ImageTk.PhotoImage(self.black_image)
        self.white_king_image = ImageTk.PhotoImage(self.white_king_image)
        self.black_king_image = ImageTk.PhotoImage(self.black_king_image)

    def place_pieces(self):
        for x in range(8):
            for y in range(8):
                pos = self.ranks[y] + str(x + 1)
                if (x + y) % 2 != 0:
                    piece = self.game.board[x][y]
                    if piece == 'b':
                        self.squares[pos].config(image=self.black_image, width=80, height=80)
                        self.squares[pos].image = self.black_image
                    elif piece == 'r':
                        self.squares[pos].config(image=self.white_image, width=80, height=80)
                        self.squares[pos].image = self.white_image
                    elif piece == 'B':
                        self.squares[pos].config(image=self.black_king_image, width=80, height=80)
                        self.squares[pos].image = self.black_king_image
                    elif piece == 'R':
                        self.squares[pos].config(image=self.white_king_image, width=80, height=80)
                        self.squares[pos].image = self.white_king_image
                    else:
                        self.squares[pos].config(image='', width=11, height=5)  # Clear previous piece image
                else:
                    self.squares[pos].config(width=11, height=5)  # Set default size

    def select_square(self, x, y):
        if self.selected_piece:
            if (x, y) in self.valid_moves:
                if self.game.move_piece(self.selected_piece, (x, y)):
                    self.clear_highlights()
                    self.selected_piece = None
                    self.valid_moves = []
                    self.place_pieces()
            else:
                self.clear_highlights()
                self.selected_piece = None
                self.valid_moves = []
        else:
            if self.game.has_piece((x, y)):
                self.selected_piece = (x, y)
                self.valid_moves = self.game.get_valid_moves((x, y))
                self.highlight_valid_moves(self.valid_moves)

    def highlight_valid_moves(self, moves):
        for (x, y) in moves:
            self.squares[self.ranks[y] + str(x + 1)].config(bg="light green")
   
    def clear_highlights(self):
        for (x, y) in self.valid_moves:
            self.squares[self.ranks[y] + str(x + 1)].config(bg=self.get_square_color(x, y))

    def get_square_color(self, x, y):
        return "tan4" if (x + y) % 2 == 0 else "burlywood1"

# Main application
class CheckersApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checkers Game")
        self.create_background()  # New method to create the background
        self.create_buttons()  # New method to create buttons
        self.game = Checkers()
        self.board = Board(self.canvas, self.game, 8, 8, "light grey", 5, "black")  # Pass canvas as parent

    def create_background(self):
        # Load the background image
        self.bg_image = Image.open("D:\\Hitha\\Checkers\\Checkers\\background1.png")  # Ensure the path is correct
        self.bg_image = self.bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to display the background image
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)

        # Place the background image on the canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_buttons(self):
        # Add buttons for help, restart, and exit to the main window
        top_frame = Frame(self.canvas, bg="lightgrey")
        top_frame.pack(side=tk.TOP)
        self.canvas.create_window((0, 0), window=top_frame, anchor="nw")

        restart_button = Button(top_frame, fg="blue", text="Restart", command=self.restart_game)
        restart_button.pack(side=tk.LEFT)

        help_button = Button(top_frame, fg="blue", text="Help", command=help)
        help_button.pack(side=tk.LEFT)

        exit_button = Button(top_frame, fg="red", text="Exit", command=self.quit)
        exit_button.pack(side=tk.RIGHT)

    def restart_game(self):
        self.board.destroy()
        self.game = Checkers()
        self.board = Board(self.canvas, self.game, 8, 8, "light grey", 5, "black")  # Pass canvas as parent

# GUI for the Checkers game (your existing Board class here)

# Main application
if __name__ == "__main__":
    app = CheckersApp()
    app.mainloop()