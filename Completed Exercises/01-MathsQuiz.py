# TKinter is a python library. First, import the module.
# Import everything from the library.
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Function to display the greeting
def switch_to_frame(frame):
    frame.tkraise()

def backTo():
    # To display the message on information message box
    messagebox.showinfo("Return", "Return to main screen?")

#create the root/output window
root = Tk()

# This window requires a title. Create a title in the output.
root.title('Maths Quiz ₊˚ 📈 ⟡📏｡ ˚')

root.geometry('400x335')
# Creates an output window of size 350 x 600

root.resizable(0, 0) # Output Window Size is fixed

#### Difficulty Menu ####

### Create the frame that holds the main difficulty menu.
main = Frame(root)
main.place(width = 400, height = 335)

### Difficulty menu GUI
img = ImageTk.PhotoImage(Image.open("MainBG.jpg"))
imgLabel = Label(main, image=img)
imgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

### Display difficulty menu
## Title displayed on the page
title = Label(
    main,
    text="MATHS QUIZ",
    font=("Courier", 28, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 11
)
title.place(x = 200, y = 50.5, anchor = "center")

## Menu panel that the heading and buttons will be placed in.
menu = Frame(
    main,
    bg = "#FFFFFF",
    width=345,
    height=215
)
menu.place(x = 200, y = 202, anchor = "center")

## Heading for the difficulty selection section
difficulty = Label(
    menu,
    text = "Difficulty Level",
    font = ("Courier", 18, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
difficulty.place(x = 175, y = 37, anchor = "center")

## Difficulty buttons
easyButton = Button(
    menu,
    text = "Easy",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: switch_to_frame(easy)
)
easyButton.place(x = 175, y = 87, anchor = "center")

modButton = Button(
    menu,
    text = "Moderate",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: switch_to_frame(mod)
)
modButton.place(x = 175, y = 128, anchor = "center")

advButton = Button(
    menu,
    text = "Advanced",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: switch_to_frame(adv)
)
advButton.place(x = 175, y = 170, anchor = "center")

#### Creating the frames.
# Frames are techincally different pages to the application

### Create the easy quiz page. 
easy = Frame(root)
easy.place(width = 400, height = 335)

easyimg = ImageTk.PhotoImage(Image.open("easyBG.jpg"))
easyimgLabel = Label(easy, image=easyimg)
easyimgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

### Easy mode GUI

## Page heading
easyTitle = Label(
    easy,
    text = "𐙚 EASY MODE 𐙚",
    font = ("Courier", 20, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
)
easyTitle.place(x = 154, y = 25, width = 228, height = 50)

area = Label(
    easy,
    font = ("Courier", 20, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
)
area.place(x = 154, y = 83, width = 228, height = 230)

question = Label(
    area,
    text = ('Question 1: '),
    font = ("Courier", 20, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
)
question.place()

prog = Label(
    easy,
    font = ("Courier", 20, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
)
prog.place(x = 19, y = 24, width = 124, height = 289)

### Create moderate quiz page
mod = Frame(root)
mod.place(width = 400, height = 335)

modimg = ImageTk.PhotoImage(Image.open("modBG.jpg"))
modimgLabel = Label(mod, image=modimg)
modimgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

### Create advanced quiz page
adv = Frame(root)
adv.place(width = 400, height = 335)

advimg = ImageTk.PhotoImage(Image.open("advBG.png"))
advimgLabel = Label(adv, image=advimg)
advimgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Initially, show the main difficulty menu
switch_to_frame(main)

# Keeps the window running and operational until manually closed.
root.mainloop()