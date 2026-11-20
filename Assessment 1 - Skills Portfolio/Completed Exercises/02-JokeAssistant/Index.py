##### Import the libraries needed for the joke-telling assistant

# import tkinter to emable GUI elements.
from tkinter import *

# Import messagebox to display pop-up messages.
from tkinter import messagebox

# import random to select random jokes from the provided text file.
import random

# import PIL to add a background image to the window.
from PIL import Image, ImageTk

#### Create the main application window

main = Tk()
main.title("Alexa's Joke Corner") # Set the window title.
main.geometry("400x350") # Set the window size.
main.configure(bg = "#FFF1DB") # Set the background colour.
main.resizable(False, False) # Prevent the user from resizing the window.

# Asign a new .ico file to the window to change it's icon.
main.iconbitmap("Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/BooksLOGO.ico")

#### Reading the jokes from the text file

# Open the randomJokes.txt file in read mode.
file = open("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt", "r")
jokes = file.readlines() # Read all the jokes and store them in a list.
file.close() # Close the file after reading.

#### Creating the functions

# Create a variable to store the current joke.
current_setup = ""
current_punchline = ""

# Function to select and display a random joke.
def get_joke():
    global current_setup, current_punchline

    # Select a random joke from the list.
    joke = random.choice(jokes)
    # Separate the setup and punchline using the question mark.
    parts = joke.strip().split("?", 1)

    current_setup = parts[0] + "?"
    current_punchline = parts[1]

    # Display the joke setup.
    joke_label.config(text = current_setup)

    # Display the Tell me button.
    request_button.place(x = 145, y = 240, width = 110, height = 35)

    # Hide the laughing dialogue and Show Question button.
    laugh_label.place_forget()
    question_button.place_forget()

# Function to display the punchline
def show_punchline():

    # Display the current joke's punchline.
    joke_label.config(text = current_punchline)

    # Hide the Tell me button.
    request_button.place_forget()

    # Display the laughing dialogue.
    laugh_label.place(x = 95, y = 240, width = 210, height = 35)

    # Display the Show Question button.
    question_button.config(text = "Show Question")
    question_button.place(x = 205, y = 300, width = 160, height = 35)

    # Set the button command.
    question_button.config(command = show_question)

# Function to display the question again.
def show_question():

    # Display the current joke's setup.
    joke_label.config(text = current_setup)

    # Change the button text to Show Joke.
    question_button.config(text = "Show Joke")

    # Set the button command to show the punchline.
    question_button.config(command = show_punchline)

# Function to confirm whether the user wants to exit.
def confirm_exit():

    # Display an exit confirmation pop-up.
    answer = messagebox.askyesno("Exit?", "Confirm exit?")

    # Close the application if the user clicks Yes.
    if answer:
        main.destroy()

#### Setting the background image

# Open the background image.
image = Image.open("Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/JokeBG.jpg")

# Resize the image to fit the window.
image = image.resize((400, 350))

# Convert the image into a Tkinter-compatible format.
bg_image = ImageTk.PhotoImage(image)

# Create a label to display the background.
background = Label(main, image = bg_image)
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

##### Designing the main interface

# Create the title label.
title_label = Label(
    main,
    text = "Alexa's Joke Corner",
    font = ("Courier", 16, "bold"),
    bg = "#E8DDCC",
    fg = "#40352C"
)
# Position the title label.
title_label.place(x = 25, y = 20, width = 350, height = 60)

# Create the label where the joke will appear.
joke_label = Label(
    main,
    text = "Your joke will appear here",
    font = ("Courier", 12),
    bg = "#E8DDCC",
    fg = "#40352C",
    wraplength = 290,
    justify = CENTER
)
# Position the joke label.
joke_label.place(x = 35, y = 95, width = 330, height = 80)

# Create the button that triggers the joke on click.
joke_button = Button(
    main,
    text = "Alexa, tell me a joke",
    font = ("Courier", 11, "bold"),
    bg = "#B99A7C",
    fg = "#FFFFFF",
    command = get_joke
)
# Position the joke button.
joke_button.place(x = 50, y = 190, width = 300, height = 40)

# Create the request button.
request_button = Button(
    main,
    text = "Tell me.",
    font = ("Courier", 11, "bold"),
    bg = "#B99A7C",
    fg = "white",
    command = show_punchline
)

# Create the laughing dialogue as a label.
laugh_label = Label(
    main,
    text = "Haha, get it?",
    font = ("Courier", 12),
    bg = "#E8DDCC",
    fg = "#40352C",
)

# Create the Exit button.
exit_button = Button(
    main,
    text = "Exit",
    font = ("Courier", 10),
    bg = "#A88A70",
    fg = "#FFFFFF",
    command = confirm_exit
)
# Position the Exit button.
exit_button.place(x = 35, y = 300, width = 130, height = 35)

# Create the Show Question / Show Joke button.
question_button = Button(
    main,
    text = "Show Question",
    font = ("Georgia", 10),
    bg = "#A88A70",
    fg = "#FFFFFF",
)

#### Set the initial button visibility

# Hide the Why and Show Question buttons initially.
request_button.place_forget()
question_button.place_forget()

# Keep the application running until the window is closed.
main.mainloop()