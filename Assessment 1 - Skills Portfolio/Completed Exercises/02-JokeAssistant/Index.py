##### Import the libraries needed for the joke-telling assistant.
# import tkinter to emable GUI elements.
from tkinter import *
# import random to select random jokes from the provided text file.
import random
# import PIL to add backgrounds to the window.
from PIL import Image, ImageTk

#### Create the main application window

main = Tk()
main.title("Alexa's Joke Corner") # Set the window title
main.geometry("400x350") # Set the window size
main.configure(bg = "#FFF1DB") # Set the background colour
main.resizable(False, False) # Prevent the user from resizing the window. Keep the fixed size.

#### Setting the background image.

image = Image.open("Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/JokeBG.jpg") # Open the background image
image = image.resize((400, 350)) # Resize the image to fit the window
bg_image = ImageTk.PhotoImage(image) # Convert the image into a Tkinter-compatible format

background = Label(main, image = bg_image) # Create a label to display the background
background.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Position the background to fill the window

main.mainloop()