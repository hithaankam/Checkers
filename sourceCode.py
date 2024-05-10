from tkinter import *
import string

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
        self.pack()
        self.square_color = None
        self.squares = {}
        self.ranks = string.ascii_lowercase

    def set_squares(self): 
        for x in range(8):
            for y in range(8):
                if x % 2 == 0 and y % 2 == 0: 
                    self.square_color = "tan4" 
                elif x % 2 == 1 and y % 2 == 1:
                    self.square_color = "tan4"
                else:
                    self.square_color = "burlywood1"
                    
                B = Button(self, bg=self.square_color, activebackground="lawn green")
                B.grid(row=8-x, column=y)
                pos = self.ranks[y]+str(x+1)
                self.squares.setdefault(pos, B)
                self.squares[pos].config(command=lambda key=self.squares[pos]: self.select_piece(key))

# Create the Tkinter window
board_root = Tk()
board_root.title("CHECKERS")
board_root.geometry("800x800")
board_root.minsize(500, 500)

# Create an instance of the Board class with a dark brown background color and a thick black border
board = Board(board_root, 8, 8, "light grey", 5, "black")

# Call the set_squares() method to populate the board with squares/buttons
board.set_squares()

# Run the Tkinter event loop
board.mainloop()
