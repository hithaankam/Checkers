from tkinter import *
from tkinter import messagebox  # Import messagebox module
import string

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

class Board(Frame):
    def __init__(self, parent, length, width, background_color="brown", border_thickness=5, border_color="black"): 
        Frame.__init__(self, parent)
        self.parent = parent
        self.length = length
        self.width = width
        self.background_color = background_color
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.config(height=1000*self.length, width=1000*self.width, bg=self.background_color, highlightthickness=self.border_thickness, highlightbackground=self.border_color)
        self.pack(side=BOTTOM)  # Placing the board at the bottom
        self.square_color = None
        self.squares = {}
        self.ranks = string.ascii_lowercase
        self.pieces = {}  # Dictionary to store pieces
        self.piece_radius = 20  # Radius of the piece

    def set_squares(self): 
        for x in range(8):
            for y in range(8):
                if x % 2 == 0 and y % 2 == 0: 
                    self.square_color = "tan4" 
                elif x % 2 == 1 and y % 2 == 1:
                    self.square_color = "tan4"
                else:
                    self.square_color = "burlywood1"
                    
                label = Label(self, bg=self.square_color, width=4, height=2)
                label.grid(row=8-x, column=y)
                pos = self.ranks[y]+str(x+1)
                self.squares.setdefault(pos, label)
    
    def add_piece(self, position, color):
        x, y = self.get_coordinates(position)
        piece = Canvas(self, width=self.piece_radius*2, height=self.piece_radius*2, bg=self.background_color, highlightthickness=0)
        piece.create_oval(0, 0, self.piece_radius*2, self.piece_radius*2, fill=color)
        piece.grid(row=8-x, column=y)  # Corrected row and column indices
        self.pieces[position] = piece

    def get_coordinates(self, position):
        y = ord(position[0]) - ord('a')
        x = int(position[1]) - 1
        return x, y

# Create the Tkinter window
board_root = Tk()
board_root.title("CHECKERS")
board_root.geometry("400x400")
board_root.minsize(400, 400)

# Add buttons for help, restart, and exit to the main window
top_frame = Frame(board_root)
top_frame.pack(side=TOP)

restart_button = Button(top_frame, fg="blue", text="Restart")
restart_button.pack(side=LEFT)

help_button = Button(top_frame, fg="blue", text="Help", command=help)
help_button.pack(side=LEFT)

exit_button = Button(top_frame, fg="red", text="Exit", command=board_root.quit)
exit_button.pack(side=RIGHT)

# Create an instance of the Board class with a light grey background color and a thick black border
board = Board(board_root, 8, 8, "light grey", 5, "black")

# Call the set_squares() method to populate the board with squares/buttons
board.set_squares()

# Add some pieces to the board
board.add_piece("a1", "red")
board.add_piece("b2", "blue")

# Run the Tkinter event loop
board_root.mainloop()