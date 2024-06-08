import tkinter as tk
from PIL import Image, ImageTk
import sys

def exit_game():
    new_root.destroy()

if len(sys.argv) > 1:
    winner = sys.argv[1]
    print("Winner:", winner)
else:
    print("No winner provided.")

new_root = tk.Tk()
new_root.title("GAME OVER")
new_root.configure(bg='grey')
new_root.minsize(1500, 1000)

player1_image_path = r"D:\Hitha\Checkers\Checkers\win1.jpeg"
player1_image = Image.open(player1_image_path)

player2_image_path = r"D:\Hitha\Checkers\Checkers\win2.jpeg"
player2_image = Image.open(player2_image_path)

draw_path = r"D:\Hitha\Checkers\Checkers\draw.jpg"
draw_image = Image.open(draw_path)

new_width = 1600
new_height = 900
if winner == "Red":
    image = player1_image
elif winner == "Black":
    image = player2_image
else:
    image = draw_image

photo = ImageTk.PhotoImage(image)
image_label = tk.Label(new_root, image=photo)
image_label.image = photo
image_label.place(x=0, y=0)

exit_button = tk.Button(new_root, fg="yellow",bg = "black",text="GO BACK",font=('Verdana', 16, 'bold'), command=exit_game, width=20, height=3, borderwidth=5, relief=tk.RAISED, highlightbackground="black") 
exit_button.pack()

new_root.mainloop()
