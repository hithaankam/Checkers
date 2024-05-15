import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Frame, Button
from tkinter import messagebox  # Import messagebox module
import os

def help():
    help_text = '''\n● Checkers is a two-player, with a dark square in each player's lower left corner.
\n● Pieces move only on dark squares which are numbered. Numbers are used to record the
moves, for example, if Red moves from square 9 to square 13, then it is recorded as:
9-13.
\n● Each player controls its own army of pieces (men). The player who controls Red pieces
moves first. The pieces (also known as 'men') are arranged as shown on the left.
\n● The goal in the checkers game is either to capture all of the opponent's pieces or to
blockade them. If neither player can accomplish the above game is a draw.'''
    messagebox.showinfo("Help", help_text)  # Display help text in a messagebox

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
        self.set_squares()

    def set_squares(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:  # Alternating square colors
                    self.square_color = "tan4"
                else:
                    self.square_color = "burlywood1"

                B = tk.Button(self, bg=self.square_color, activebackground="lawn green")
                B.grid(row=8 - x, column=y)
                pos = self.ranks[y] + str(x + 1)
                self.squares.setdefault(pos, B)
    
    def load_piece_images(self):
        # Load white and black piece images
        white_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "white_piece.png")
        black_piece_image_path = os.path.join(os.path.dirname(__file__), "Checkers", "black_piece.png")
        self.white_image = Image.open(white_piece_image_path)
        self.black_image = Image.open(black_piece_image_path)

    def place_pieces(self):
        for x in range(8):
            for y in range(8):
                pos = self.ranks[y] + str(x + 1)
                if (x + y) % 2 != 0:  # Only on alternate squares
                    if 0 <= x < 3:  # Place black pieces
                        piece = ImageTk.PhotoImage(self.black_image)
                        self.squares[pos].config(image=piece, width=80, height=80)  # Adjust size only for squares with pieces
                        self.squares[pos].image = piece
                    elif 5 <= x < 8:  # Place white pieces
                        piece = ImageTk.PhotoImage(self.white_image)
                        self.squares[pos].config(image=piece, width=80, height=80)  # Adjust size only for squares with pieces
                        self.squares[pos].image = piece
                    else:
                        self.squares[pos].config(width=11, height=5) 
                else:
                    self.squares[pos].config(width=11, height=5)  # Maintain square size for empty squares

root = tk.Tk()
root.title("Checkers Game")

# Add buttons for help, restart, and exit to the main window
top_frame = Frame(root)
top_frame.pack(side=tk.TOP)

restart_button = Button(top_frame, fg="blue", text="Restart")
restart_button.pack(side=tk.LEFT)

help_button = Button(top_frame, fg="blue", text="Help", command=help)
help_button.pack(side=tk.LEFT)

exit_button = Button(top_frame, fg="red", text="Exit", command=root.quit)
exit_button.pack(side=tk.RIGHT)


board = Board(root, 8, 8, "light grey", 5, "black")
board.load_piece_images()
board.place_pieces()
root.mainloop()
