# TKinter is a python library. First, import the module.
# Import everything from the library.
from tkinter import * 
from PIL import ImageTk, Image

#create the root/output window
root = Tk()

# This window requires a title. Create a title in the output.
root.title('Maths Quiz')

root.geometry('400x400')
# Creates an output window of size 350 x 600

root.resizable(0, 0) # Output Window Size is fixed

## Difficulty Menu ##

# Difficulty menu GUI
img = ImageTk.PhotoImage(Image.open("MainBG.jpg"))
imgLabel = Label(root, image=img)
imgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Display difficulty menu
title = Label(
    root,
    text="MATHS QUIZ",
    font=("Times New Roman", 28, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
title.place(x = 200, y = 60, anchor = "center")

menu = Frame(
    root,
    bg = "#FFFFFF",
    width=350,
    height=261.5
)
menu.place(x = 200, y = 240, anchor = "center")

difficulty = Label(
    menu,
    text = "Select Difficulty",
    font = ("Times New Roman", 16, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
difficulty.place(x = 175, y = 40, anchor = "center")

root.mainloop() # This is the closing bracket that always stays at the end of the code.