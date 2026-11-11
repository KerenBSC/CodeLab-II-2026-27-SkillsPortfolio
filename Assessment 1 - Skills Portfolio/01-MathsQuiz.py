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

#### Difficulty Menu ####

### Difficulty menu GUI
img = ImageTk.PhotoImage(Image.open("MainBG.jpg"))
imgLabel = Label(root, image=img)
imgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

### Display difficulty menu
## Title displayed on the page
title = Label(
    root,
    text="MATHS QUIZ",
    font=("Courier", 28, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 11
)
title.place(x = 200, y = 55, anchor = "center")

## Menu panel that the heading and buttons will be placed in.
menu = Frame(
    root,
    bg = "#FFFFFF",
    width=340,
    height=262
)
menu.place(x = 200, y = 235, anchor = "center")

## Heading for the difficulty selection section
difficulty = Label(
    menu,
    text = "Difficulty Level",
    font = ("Courier", 18, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
difficulty.place(x = 175, y = 55, anchor = "center")

## Difficulty buttons
easyButton = Button(
    menu,
    text = "Easy",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10
)
easyButton.place(x = 175, y = 105, anchor = "center")

modButton = Button(
    menu,
    text = "Moderate",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10
)
modButton.place(x = 175, y = 150, anchor = "center")

advButton = Button(
    menu,
    text = "Advanced",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10
)
advButton.place(x = 175, y = 195, anchor = "center")

root.mainloop() # This is the closing bracket that always stays at the end of the code.