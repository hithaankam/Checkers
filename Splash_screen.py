import tkinter as tk

# Create the main window
splash_root = tk.Tk()
splash_root.title("Checkers Game")
splash_root.geometry("1600x900")

# Load the background image
background_image = tk.PhotoImage(file="background_image.png")

# Create a label with the background image
background_label = tk.Label(splash_root, image=background_image,bg = "#9A7B4F")
background_label.place(x=0, y=0, relwidth=1, relheight=1, anchor = "nw")

# Create a title label with "Courier New" font and expanded width
title_label = tk.Label(splash_root, text="Checkers", font=("Courier New", 100, "bold") )
title_label.pack(expand=True)


# Remove window decorations
splash_root.overrideredirect(True)

# Close the splash screen after 5000 milliseconds (5 seconds)
splash_root.after(5000, splash_root.destroy)

# Start the Tkinter main loop
splash_root.mainloop()

import tkinter as tk