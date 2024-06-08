import tkinter as tk
from tkinter import Frame, Button, messagebox, simpledialog, Toplevel
from PIL import Image, ImageTk
import subprocess
from tkinter import ACTIVE
from tkinter import LEFT
import pygame
import json

pygame.mixer.init()

button_sound = pygame.mixer.Sound(r"C:\Users\nalin\OneDrive\Desktop\Checkers\button-click_sound.mp3")
capture_sound = pygame.mixer.Sound(r"C:\Users\nalin\OneDrive\Desktop\Checkers\killing_sound.mp3")
king_sound = pygame.mixer.Sound(r"C:\Users\nalin\OneDrive\Desktop\Checkers\making_king_sound.wav")
sound=pygame.mixer.Sound(r"C:\Users\nalin\OneDrive\Desktop\Checkers\sound.wav")
class PlayerDialog(simpledialog.Dialog):
    def body(self, master):
        dialog_width = 500 
        dialog_height = 200  

        master.configure(bg="#802000", relief="groove", borderwidth=10)
       
        self.minsize(dialog_width, dialog_height)
        self.maxsize(dialog_width, dialog_height)

        tk.Label(master, text="Player 1:", font=("Helvetica", 20), relief="groove", borderwidth=10).grid(row=0, sticky="w")
        tk.Label(master, text="Player 2:", font=("Helvetica", 20), relief="groove", borderwidth=10).grid(row=1, sticky="w")

        frame = tk.Frame(master, bg="#802000", relief="groove", borderwidth=10)
        frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5)
        self.player1_entry = tk.Entry(frame, font=("Helvetica", 20), bg='white')
        self.player2_entry = tk.Entry(frame, font=("Helvetica", 20), bg='white')

        self.player1_entry.grid(row=0, column=0, sticky="ew", padx=30, pady=5)
        self.player2_entry.grid(row=1, column=0, sticky="ew", padx=30, pady=5)

        return self.player1_entry
    
    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, font=("Helvetica", 14), command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        w = Button(box, text="Cancel", width=10, font=("Helvetica", 14), command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.player1 = self.player1_entry.get()
        self.player2 = self.player2_entry.get()

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
                if (i + j) % 2 == 2:
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
            capture_sound.play()

        self.board[ex][ey] = self.board[sx][sy]
        self.board[sx][sy] = ' '

        self.check_king(ex, ey)

        self.current_turn = 'b' if self.current_turn == 'r' else 'r'
        self.check_game_over()
    
        return True

    def check_king(self, x, y):
        if self.board[x][y] == 'r' and x == 7:
            self.board[x][y] = 'R'
            make_king_sound.play()
        elif self.board[x][y] == 'b' and x == 0:
            self.board[x][y] = 'B'
            king_sound.play()

    def check_winner(self):
        r_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        b_pieces = sum(row.count('b') + row.count('B') for row in self.board)
    
        if r_pieces == 0:
            print(r_pieces)
            return 'Black'
        elif b_pieces == 0:
            return 'Red'
        
        if not (self.get_valid_moves((x, y)) for x in range(8) for y in range(8) if self.board[x][y].lower() == 'r'):
            print(True)
            return 'Black'
        if not (self.get_valid_moves((x, y)) for x in range(8) for y in range(8) if self.board[x][y].lower() == 'b'):
            return 'Red'
        
        return None

    def check_draw(self):
        r_moves = any(self.get_valid_moves((x, y)) for x in range(8) for y in range(8) if self.board[x][y].lower() == 'r')
        b_moves = any(self.get_valid_moves((x, y)) for x in range(8) for y in range(8) if self.board[x][y].lower() == 'b')

        if not r_moves and not b_moves:
            return True
        return False

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            self.show_game_over_screen(winner)
        elif self.check_draw():
            self.show_game_over_screen("draw")
            

    def show_game_over_screen(self, winner):
        sound.play()
        board_state = json.dumps(self.board)
        subprocess.Popen(["python", r"C:\Users\nalin\OneDrive\Desktop\Checkers\ending.py", str(winner), board_state])



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
    def __init__(self, parent, game, update_turn_display, length, width, background_color, border_thickness, border_color):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.game = game
        self.update_turn_display = update_turn_display
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
        self.white_image = Image.open(r"C:\Users\nalin\OneDrive\Desktop\Checkers\white_image_e.png")
        self.black_image = Image.open(r"C:\Users\nalin\OneDrive\Desktop\Checkers\black_image_e.png")
        self.white_king_image = Image.open(r"C:\Users\nalin\OneDrive\Desktop\Checkers\wking.jpeg")
        self.black_king_image = Image.open(r"C:\Users\nalin\OneDrive\Desktop\Checkers\bking.jpeg")  

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
                        self.squares[pos].config(image='', width=11, height=5)  
                else:
                    self.squares[pos].config(width=11, height=5)  

    def select_square(self, x, y):
        button_sound.play()
        if self.selected_piece:
            if (x, y) in self.valid_moves:
                if self.game.move_piece(self.selected_piece, (x, y)):
                    self.clear_highlights()
                    self.selected_piece = None
                    self.valid_moves = []
                    self.place_pieces()
                    self.update_turn_display()
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
    def __init__(self, player1, player2):
        tk.Tk.__init__(self)
        self.player1 = player1
        self.player2 = player2
        self.title("Checkers Game")
        self.create_turn_display()
        self.create_background()
        self.create_side_buttons()
        self.game = Checkers()
        self.board = Board(self.canvas, self.game, self.update_turn_display, 8, 8, "light grey", 5, "black")

    def create_background(self):
        self.bg_image = Image.open(r"C:\Users\nalin\OneDrive\Desktop\Checkers\background.jpg")
        self.bg_image = self.bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def create_side_buttons(self):
        button_frame = Frame(self.canvas, bg = "#80471C")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.canvas.create_window((self.winfo_screenwidth(), 0), window=button_frame, anchor="ne")

        restart_button = Button(button_frame, fg="yellow",bg = "black",text="Restart",font=('Verdana', 16, 'bold'),  width=10, height=4, command=self.restart_game)
        restart_button.pack(side=tk.TOP, pady=5)

        help_button = Button(button_frame, fg="yellow",bg = "black", text="Help",font=('Verdana', 16, 'bold'),  width=10, height=4, command=help)
        help_button.pack(side=tk.TOP, pady=5)

        exit_button = Button(button_frame, fg="yellow", bg = "black", text="Exit",font=('Verdana', 16, 'bold'),  width=10, height=4, command=self.quit)
        exit_button.pack(side=tk.TOP, pady=5)

    def update_turn_display(self):
        current_player = self.player1 if self.game.current_turn == 'r' else self.player2
        color = "White" if self.game.current_turn == 'r' else "Black"
        self.turn_label.config(text=f"Current Turn: {current_player} ({color})")

    def restart_game(self):
        self.board.destroy()
        self.game = Checkers()
        self.board = Board(self.canvas, self.game, self.update_turn_display, 8, 8, "light grey", 5, "black")
        self.update_turn_display()

    def create_turn_display(self):
        self.turn_frame = tk.Frame(self, bg="#80471C")
        self.turn_frame.pack(side="top", fill="x")
        self.turn_label = tk.Label(self.turn_frame, text=f"Current Turn: {self.player1} (White)", font=('Verdana', 16, 'bold'), bg="#80471C", fg="yellow")
        self.turn_label.pack()



def main():
    sound.play()
    new_root = tk.Tk()
    new_root.title("Checkers")
    new_root.minsize(1600, 900)
    image_path = r"C:\Users\nalin\OneDrive\Desktop\Checkers\background.jpg"
    image = Image.open(image_path)
    new_width = 1600
    new_height = 900
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    image_label = tk.Label(new_root, image=photo)
    image_label.place(x=0, y=0)

    dialog = PlayerDialog(new_root, title="Enter Player Names")
    player1 = dialog.player1
    player2 = dialog.player2

    print("Player 1:", player1)
    print("Player 2:", player2)

    #new_root.mainloop()
    new_root.destroy()

    app = CheckersApp(player1, player2)
    app.mainloop()
    
main()
