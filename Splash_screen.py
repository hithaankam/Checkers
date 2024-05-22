import tkinter as tk
from PIL import Image, ImageTk
import subprocess

def start_button_clicked():
    print("START button clicked!")
    run_source_code()

def run_source_code():
    try:
        subprocess.Popen(["python", "D:\Hitha\Checkers\Checkers\sourceCode.py"])
        new_root.after(100, close_welcome_page)
    except Exception as e:
        print("An error occurred while running the source code:", e)

def close_welcome_page():
    new_root.destroy()

new_root = tk.Tk()
new_root.title("CHECKERS")
new_root.configure(bg='grey')
new_root.minsize(1500, 1000)

image_path = "D:\\Hitha\\Checkers\\Checkers\\welcome_image.png"
image = Image.open(image_path)
new_width = 1600
new_height = 900
resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(new_root, image=photo)
image_label.place(x=0, y=0)

start_button = tk.Button(
    new_root, 
    text="START", 
    command=start_button_clicked, 
    width=20, 
    height=2, 
    font=('Verdana', 16, 'bold'), 
    padx=5, 
    pady=5,   
    relief='groove', 
    bg='black', 
    fg='red' 
)
start_button.place(x=600, y=600)

new_root.mainloop()
