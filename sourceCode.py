import tkinter as tk
from tkinter import Frame, Button, messagebox
import os

def help():
    help_text = '''\n● Checkers is a two-player game, with a dark square in each player's lower left corner.
\n● Pieces move only on dark squares which are numbered. Numbers are used to record the
moves, for example, if Red moves from square 9 to square 13, then it is recorded as:
9-13.
\n● Each player controls its own army of pieces (men). The player who controls Red pieces
moves first. The pieces (also known as 'men') are arranged as shown on the left.
\n● The goal in the checkers game is either to capture all of the opponent's pieces or to
blockade them. If neither player can accomplish the above game is a draw.'''
    messagebox.showinfo("Help", help_text)

class Board(tk.Frame):

    def __init__(self, parent, length, width, background_color, border_thickness, border_color):
        tk.Frame.__init__(self, parent)
        self.parent = parent
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
        self.selected_piece = None
        self.turn = "black"  
        self.set_squares()
        self.turn_label = tk.Label(parent, text="Turn: Black", font=("Arial", 14), bg=background_color)
        self.turn_label.pack(side=tk.TOP, pady=5)

        self.status_label = tk.Label(parent, text="", font=("Arial", 14), bg=background_color)
        self.status_label.pack(side=tk.TOP, pady=5)

    def set_squares(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:  
                    self.square_color = "white"
                else:
                    self.square_color = "#D0312D"

                B = tk.Button(self, bg=self.square_color, activebackground="#ADD8E6", command=lambda row=x, col=y: self.on_button_click(row, col))
                B.grid(row=8 - x, column=y)
                pos = self.ranks[y] + str(x + 1)
                self.squares[pos] = B
    
    def load_piece_images(self):

        white_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "white_piece.png")
        black_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "black_piece.png")
        self.white_image = tk.PhotoImage(file=white_piece_image_path)
        self.black_image = tk.PhotoImage(file=black_piece_image_path)


    def place_pieces(self):
        for x in range(8):
            for y in range(8):
                pos = self.ranks[y] + str(x + 1)
                if (x + y) % 2 == 0:  
                    if 0 <= x < 3:  
                        self.squares[pos].config(image=self.black_image, width=80, height=80)
                        self.squares[pos].piece = "black"
                    elif 5 <= x < 8:  
                        self.squares[pos].config(image=self.white_image, width=80, height=80)
                        self.squares[pos].piece = "white"
                    else:
                        self.squares[pos].config(width=11, height=5)
                        self.squares[pos].piece = None
                else:
                    self.squares[pos].config(width=11, height=5)
                    self.squares[pos].piece = None

    def on_button_click(self, row, col):
        pos = self.ranks[col] + str(row + 1)
        if self.selected_piece:
            self.select_square(row, col)
        elif self.squares[pos].piece and self.squares[pos].piece == self.turn:
            self.select_piece(row, col)

    def select_piece(self, row, col):
        pos = self.ranks[col] + str(row + 1)
        self.selected_piece = pos
        self.highlight_valid_moves(pos)

    def select_square(self, row, col):
        pos = self.ranks[col] + str(row + 1)
        if pos in self.valid_moves:
            self.move_piece(row, col, pos)
            self.reset_square_colors()
            self.selected_piece = None
            self.valid_moves = {}

    def highlight_valid_moves(self, pos):
        x, y = int(pos[1]) - 1, self.ranks.index(pos[0])
        piece = self.squares[pos].piece
        self.valid_moves = {}

        directions = [(-1, -1), (-1, 1)] if piece == "black" else [(1, -1), (1, 1)]
        if hasattr(self.squares[pos], 'king') and self.squares[pos].king:
            directions += [(-d[0], -d[1]) for d in directions]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                new_pos = self.ranks[new_y] + str(new_x + 1)
                if not self.squares[new_pos].piece:
                    self.squares[new_pos].config(bg="black")
                    self.valid_moves[new_pos] = "move"
                else:
                    capture_x, capture_y = new_x + dx, new_y + dy
                    if 0 <= capture_x < 8 and 0 <= capture_y < 8:
                        capture_pos = self.ranks[capture_y] + str(capture_x + 1)
                        if not self.squares[capture_pos].piece and self.squares[new_pos].piece != piece:
                            self.squares[capture_pos].config(bg="black")
                            self.valid_moves[capture_pos] = "capture"
    def check_win_condition(self):
        black_pieces = 0
        white_pieces = 0
        for pos in self.squares:
            if self.squares[pos].piece == "black":
                black_pieces += 1
            elif self.squares[pos].piece == "white":
                white_pieces += 1
        if black_pieces == 0:
            messagebox.showinfo("Game Over", "White wins! All black pieces captured.")
            self.reset_board()
        elif white_pieces == 0:
            messagebox.showinfo("Game Over", "Black wins! All white pieces captured.")
            self.reset_board()

    def check_forced_capture(self):
        forced_captures = False
        for pos in self.squares:
            if self.squares[pos].piece == self.turn:
                self.highlight_valid_moves(pos)
                if self.valid_moves:
                    forced_captures = True
                self.reset_square_colors()
        return forced_captures

    def switch_turn(self):
        self.turn = "white" if self.turn == "black" else "black"
        messagebox.showinfo("Turn", f"It's {self.turn}'s turn.")
        self.turn_label.config(text=f"Turn: {self.turn.capitalize()}")
    def check_draw_condition(self):
        # Check if there are only kings left on the board
        black_pieces = 0
        white_pieces = 0
        for pos in self.squares:
            if self.squares[pos].piece == "black" or (hasattr(self.squares[pos], 'king') and self.squares[pos].king):
                black_pieces += 1
            elif self.squares[pos].piece == "white" or (hasattr(self.squares[pos], 'king') and self.squares[pos].king):
                white_pieces += 1
        if black_pieces == 0 and white_pieces == 0:
            messagebox.showinfo("Game Over", "Draw! No pieces left on the board.")
            self.reset_board()
        elif black_pieces == 1 and white_pieces == 1:
            messagebox.showinfo("Game Over", "Draw! Only kings left on the board.")
            self.reset_board()
        self.status_label.config(text="Draw! No pieces left on the board.")



    def move_piece(self, row, col, new_pos):
        old_pos = self.selected_piece
        piece = self.squares[old_pos].piece

        # Check if the piece reaches the opposite end of the board and promote it to a king
        if (piece == "black" and row == 7) or (piece == "white" and row == 0):
            self.squares[new_pos].king = True
            self.draw_king_dot(new_pos, piece)

        self.squares[new_pos].config(image=self.black_image if piece == "black" else self.white_image, width=80, height=80)
        self.squares[new_pos].piece = piece

        self.squares[old_pos].config(image='', width=11, height=5)
        self.squares[old_pos].piece = None

        self.selected_piece = None
        self.check_win_condition()
        self.check_draw_condition()


        if not self.check_forced_capture():
            self.switch_turn()
    
    def draw_king_dot(self, pos, piece_color):
        dot_color = "white" if piece_color == "black" else "black"
        self.squares[pos].create_oval(30, 30, 50, 50, fill=dot_color)
    
    def reset_square_colors(self):
        for pos in self.squares:
            x, y = int(pos[1]) - 1, self.ranks.index(pos[0])
            if (x + y) % 2 == 0:
                self.squares[pos].config(bg="white")
            else:
                self.squares[pos].config(bg="#D0312D")

root = tk.Tk()
root.title("Checkers Game")
root.configure(bg='grey')

top_frame = Frame(root)
top_frame.pack(side=tk.TOP)

restart_button = Button(top_frame, fg="blue", text="Restart", command=lambda: [board.place_pieces(), board.reset_square_colors()])
restart_button.pack(side=tk.LEFT)

help_button = Button(top_frame, fg="blue", text="Help", command=help)
help_button.pack(side=tk.LEFT)

exit_button = Button(top_frame, fg="red", text="Exit", command=root.quit)
exit_button.pack(side=tk.RIGHT)

board = Board(root, 8, 8, "light grey", 5, "black")
board.load_piece_images()
board.place_pieces()
root.mainloop()