##### Import the libraries needed for the joke-telling assistant

# Import tkinter to enable GUI elements.
from tkinter import *

# Import messagebox to display pop-up messages.
from tkinter import messagebox

# Import random to select random jokes and reactions.
import random

# Import PIL to add and resize images.
from PIL import Image, ImageTk


#### Create the main application window

main = Tk()
main.title("Alexa's Joke Corner")
main.geometry("760x590")
main.configure(bg="#CBC0B6")
main.resizable(True, True)

# Assign an icon to the application window.
main.iconbitmap("Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/BooksLOGO.ico")


#### Creating the main application frame

# Create a frame to hold all the GUI elements.
app_frame = Frame(main, width=760, height=590, bg="#CBC0B6")
app_frame.place(x=0, y=0, width=760, height=590)


#### Creating the responsive resizing system

# Store the original window dimensions.
original_width = 760
original_height = 590

# Store the current window dimensions.
current_width = original_width
current_height = original_height

# Store the original positions and sizes of GUI elements.
widget_positions = {}

# Store the original background and mascot images.
background_original = None
mascot_originals = {}

# Store the current mascot images.
mascot_images = {}

# Store the current mascot mood.
current_mood = "happy"

# Store the last dimensions used to resize the images.
last_image_size = (original_width, original_height)


# Function to position GUI elements according to the window size.
def place_scaled(widget, x, y, width, height):

    # Store the original position and size of the widget.
    widget_positions[widget] = (x, y, width, height)

    # Calculate the resizing proportions.
    scale_x = current_width / original_width
    scale_y = current_height / original_height

    # Resize and position the widget.
    widget.place(
        x=int(x * scale_x),
        y=int(y * scale_y),
        width=max(1, int(width * scale_x)),
        height=max(1, int(height * scale_y))
    )


# Function to resize the entire interface.
def resize_gui(event):

    global current_width, current_height
    global bg_image, mascot_images, last_image_size

    # Only respond to changes in the main window.
    if event.widget == main:

        # Get the new window dimensions.
        current_width = event.width
        current_height = event.height

        # Avoid resizing when the window has no usable dimensions.
        if current_width <= 0 or current_height <= 0:
            return

        # Resize the application frame.
        app_frame.place(
            x=0,
            y=0,
            width=current_width,
            height=current_height
        )

        # Calculate the resizing proportions.
        scale_x = current_width / original_width
        scale_y = current_height / original_height

        # Resize and reposition visible GUI elements.
        for widget, position in widget_positions.items():

            # Only reposition widgets that are currently visible.
            if widget.winfo_manager() == "place":

                x, y, width, height = position

                widget.place(
                    x=int(x * scale_x),
                    y=int(y * scale_y),
                    width=max(1, int(width * scale_x)),
                    height=max(1, int(height * scale_y))
                )

                # Adjust the joke text wrapping.
                if widget == joke_label:
                    widget.config(wraplength=int(650 * scale_x))

        # Only resize images if the window dimensions have changed.
        if last_image_size != (current_width, current_height):

            # Resize the background image.
            resized_background = background_original.resize(
                (current_width, current_height),
                Image.LANCZOS
            )

            bg_image = ImageTk.PhotoImage(resized_background)
            background.config(image=bg_image)

            # Resize all mascot images.
            mascot_images = {}

            for mood in mascot_originals:

                resized_mascot = mascot_originals[mood].resize(
                    (
                        max(1, int(160 * scale_x)),
                        max(1, int(85 * scale_y))
                    ),
                    Image.LANCZOS
                )

                mascot_images[mood] = ImageTk.PhotoImage(resized_mascot)

            # Keep the currently displayed mascot expression.
            mascot_label.config(image=mascot_images[current_mood])

            # Remember the dimensions used for resizing.
            last_image_size = (current_width, current_height)


#### Creating the fullscreen function

# Create a variable to store the fullscreen state.
fullscreen = False


# Function to toggle fullscreen mode.
def toggle_fullscreen():

    global fullscreen

    if fullscreen == False:

        main.state("zoomed")
        fullscreen = True

        # Change the button text.
        fullscreen_button.config(text="Restore")

    else:

        # Return to the original window size.
        main.state("normal")

        # Centre the window on the screen.
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()

        x = (screen_width - 760) // 2
        y = (screen_height - 590) // 2

        main.geometry("760x590+" + str(x) + "+" + str(y))

        fullscreen = False

        # Change the button text.
        fullscreen_button.config(text="Fullscreen")


# Function to exit fullscreen mode using the Escape key.
def exit_fullscreen(event):

    global fullscreen

    if fullscreen == True:

        main.state("normal")

        # Centre the window on the screen.
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()

        x = (screen_width - 760) // 2
        y = (screen_height - 590) // 2

        main.geometry("760x590+" + str(x) + "+" + str(y))

        fullscreen = False
        fullscreen_button.config(text="Fullscreen")


# Bind the Escape key to exit fullscreen mode.
main.bind("<Escape>", exit_fullscreen)


#### Reading the jokes from the text file

# Open the randomJokes.txt file in read mode.
file = open("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt", "r")

# Read all the jokes and store them in a list.
jokes = file.readlines()

# Close the file after reading.
file.close()


#### Creating the variables

# Store the current joke.
current_setup = ""
current_punchline = ""

# Count the number of jokes told during the session.
jokes_told = 0

# Store the typewriter animation.
typing_job = None

# Store the number of times the title has been clicked.
title_clicks = 0

# Check whether the secret interaction has been unlocked.
secret_unlocked = False

# Store any milestone message.
milestone_message = ""


#### Creating the mascot mood function

# Function to change Alexa's mood and mascot image.
def set_mood(mood, display_text=None):

    global current_mood

    # Store the current mood.
    current_mood = mood

    # Update the mood label.
    if display_text is None:
        mood_label.config(text="Mood: " + mood.capitalize())

    else:
        mood_label.config(text=display_text)

    # Change the mascot image.
    mascot_label.config(image=mascot_images[mood])


#### Creating Alexa's personality messages

# Messages displayed before a joke.
setup_messages = [
    "I've got a good one for you!",
    "Prepare yourself. This one's funny!",
    "Okay, listen carefully...",
    "I think you're going to like this one!",
    "Another masterpiece coming right up!"
]

# Random reactions displayed after a punchline.
reactions = [
    "Haha, get it?",
    "I'm hilarious. I know.",
    "Don't laugh too hard!",
    "Okay, that one was questionable...",
    "You're welcome. I'm here all week!",
    "I really outdid myself there.",
    "HAHA! Get it? Get it?"
]


#### Creating the typewriter effect

# Function to display text one character at a time.
def type_text(text, index=0, callback=None):

    global typing_job

    # Display the text one character at a time.
    if index <= len(text):

        joke_label.config(text=text[:index])

        # Continue displaying the next character.
        typing_job = main.after(
            25,
            lambda: type_text(text, index + 1, callback)
        )

    else:

        typing_job = None

        # Run the next function after the animation finishes.
        if callback:
            callback()


# Function to start the typewriter effect.
def start_typing(text, callback=None):

    global typing_job

    # Cancel any previous typing animation.
    if typing_job is not None:
        main.after_cancel(typing_job)
        typing_job = None

    # Clear the joke label.
    joke_label.config(text="")

    # Start displaying the text.
    type_text(text, 0, callback)


#### Creating the joke functions

# Function to select and display a random joke.
def get_joke():

    global current_setup, current_punchline
    global jokes_told, milestone_message

    # Select a random joke from the list.
    joke = random.choice(jokes)

    # Separate the setup and punchline using the question mark.
    parts = joke.strip().split("?", 1)

    current_setup = parts[0] + "?"
    current_punchline = parts[1].strip()

    # Increase the joke counter.
    jokes_told += 1

    # Update the joke counter label.
    counter_label.config(text="Jokes told: " + str(jokes_told))

    # Check whether the user has reached a joke milestone.
    milestone_message = ""

    if jokes_told == 5:
        milestone_message = "5 jokes already! You're warming up!"

    elif jokes_told == 10:
        milestone_message = "10 jokes! You're officially a fan!"

    elif jokes_told == 20:
        milestone_message = "20 JOKES?! You're Alexa's biggest fan!"

    # Change the main button text.
    joke_button.config(text="Alexa, tell me another joke")

    # Temporarily disable the button.
    joke_button.config(state=DISABLED)

    # Hide the other buttons and ratings.
    request_button.place_forget()
    question_button.place_forget()
    rating_prompt.place_forget()
    rating1_button.place_forget()
    rating2_button.place_forget()
    rating3_button.place_forget()
    laugh_label.place_forget()

    # Display a thinking message.
    status_label.config(text="Hmm... let me think of something funny.")
    set_mood("thinking")

    # Clear the joke label.
    joke_label.config(text="")

    # Give Alexa a short thinking delay before displaying the joke.
    main.after(900, lambda: start_typing(current_setup, setup_finished))


# Function to run after the joke setup has finished displaying.
def setup_finished():

    # Enable the main joke button.
    joke_button.config(state=NORMAL)

    # Display a random personality message or milestone.
    if milestone_message != "":
        status_label.config(text=milestone_message)

    else:
        status_label.config(text=random.choice(setup_messages))

    set_mood("mischievous")

    # Display the Tell me button.
    place_scaled(request_button, 325, 445, 110, 35)


# Function to display the punchline.
def show_punchline():

    # Hide the Tell me button.
    request_button.place_forget()

    # Hide the rating buttons until the punchline finishes.
    rating_prompt.place_forget()
    rating1_button.place_forget()
    rating2_button.place_forget()
    rating3_button.place_forget()

    # Disable the Show Question button during the animation.
    question_button.config(state=DISABLED)

    # Update Alexa's mood.
    status_label.config(text="And here comes the best part...")
    set_mood("amused")

    # Display the punchline with the typewriter effect.
    start_typing(current_punchline, punchline_finished)


# Function to run after the punchline has finished displaying.
def punchline_finished():

    # Select a random reaction.
    laugh_label.config(text=random.choice(reactions))

    # Display the laughing dialogue where the Tell me button was.
    place_scaled(laugh_label, 200, 445, 360, 35)

    # Display the rating prompt and buttons.
    place_scaled(rating_prompt, 230, 495, 300, 25)

    place_scaled(rating1_button, 55, 535, 180, 35)
    place_scaled(rating2_button, 290, 535, 180, 35)
    place_scaled(rating3_button, 525, 535, 180, 35)

    # Display the Show Question button at the top.
    question_button.config(
        text="Show Question",
        command=show_question,
        state=NORMAL
    )

    place_scaled(question_button, 590, 10, 130, 35)


# Function to display the question again.
def show_question():

    # Disable the button while the text is appearing.
    question_button.config(state=DISABLED)

    # Hide the laughing dialogue and rating buttons.
    laugh_label.place_forget()
    rating_prompt.place_forget()
    rating1_button.place_forget()
    rating2_button.place_forget()
    rating3_button.place_forget()

    # Update Alexa's messages.
    status_label.config(text="Here's the question again!")
    set_mood("curious")

    # Display the original joke setup.
    start_typing(current_setup, question_finished)


# Function to run after the question has finished displaying.
def question_finished():

    # Change the button text and command.
    question_button.config(
        text="Show Joke",
        command=show_punchline,
        state=NORMAL
    )

    # Keep the Show Joke button at the top.
    place_scaled(question_button, 590, 10, 130, 35)

    # Display the Tell me button again.
    place_scaled(request_button, 325, 445, 110, 35)


#### Creating the joke rating function

# Function to respond to the user's joke rating.
def rate_joke(rating):

    # Store different responses depending on the rating.
    if rating == "Hilarious!":

        response = "I KNEW you'd like that one!"

    elif rating == "It was okay.":

        response = "I'll try harder next time..."

    else:

        response = "Ouch. That hurt my feelings."

    # Display Alexa's response.
    laugh_label.config(text=response)

    # Keep the mascot happy for all joke ratings.
    set_mood("happy", "Mood: " + rating)


#### Creating the secret interaction

# Function triggered when the title is clicked.
def secret_interaction(event):

    global title_clicks, secret_unlocked

    # Only unlock the secret once.
    if secret_unlocked == False:

        title_clicks += 1

        # Check whether the title has been clicked five times.
        if title_clicks == 5:

            secret_unlocked = True

            messagebox.showinfo(
                "Secret Unlocked!",
                "Congratulations!\n\n"
                "You've discovered my secret.\n"
                "Please don't tell anyone..."
            )


#### Creating the exit function

# Function to confirm whether the user wants to exit.
def confirm_exit():

    # Display an exit confirmation pop-up.
    answer = messagebox.askyesno("Exit?", "Confirm exit?")

    # Close the application if the user clicks Yes.
    if answer:
        main.destroy()


#### Setting the background image

# Open the original background image.
background_original = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/JokeBG.jpg"
)

# Resize the image to fit the original application frame.
image = background_original.resize((760, 590))

# Convert the image into a Tkinter-compatible format.
bg_image = ImageTk.PhotoImage(image)

# Create a label to display the background.
background = Label(app_frame, image=bg_image)

place_scaled(background, 0, 0, 760, 590)


#### Designing the main interface

# Create the Exit button.
exit_button = Button(
    app_frame,
    text="Exit",
    font=("Courier", 10),
    bg="#A88A70",
    fg="#FFFFFF",
    command=confirm_exit
)

place_scaled(exit_button, 40, 10, 130, 35)


# Create the fullscreen button.
fullscreen_button = Button(
    app_frame,
    text="Fullscreen",
    font=("Courier", 9, "bold"),
    bg="#A88A70",
    fg="#FFFFFF",
    command=toggle_fullscreen
)

place_scaled(fullscreen_button, 305, 10, 150, 35)


# Create the Show Question / Show Joke button.
question_button = Button(
    app_frame,
    text="Show Question",
    font=("Georgia", 10),
    bg="#A88A70",
    fg="#FFFFFF"
)


#### Creating the title label

# Create the title label.
title_label = Label(
    app_frame,
    text="Alexa's Joke Corner",
    font=("Courier", 18, "bold"),
    bg="#E8DDCC",
    fg="#40352C"
)

place_scaled(title_label, 40, 65, 680, 55)

# Bind the title to the secret interaction.
title_label.bind("<Button-1>", secret_interaction)


#### Creating the mascot area

# Load the original mascot images for each mood.
mascot_originals["happy"] = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/happy.jpg"
)

mascot_originals["amused"] = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/amused.jpg"
)

mascot_originals["curious"] = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/curious.jpg"
)

mascot_originals["mischievous"] = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/mischievous.jpg"
)

mascot_originals["thinking"] = Image.open(
    "Assessment 1 - Skills Portfolio/Completed Exercises/02-JokeAssistant/thinking.jpg"
)

# Create the initial mascot images.
for mood in mascot_originals:

    mascot_images[mood] = ImageTk.PhotoImage(
        mascot_originals[mood].resize((160, 85))
    )

# Create the mascot label.
mascot_label = Label(
    app_frame,
    image=mascot_images["happy"],
    bg="#E8DDCC"
)

place_scaled(mascot_label, 300, 140, 160, 85)


#### Creating the status and joke labels

# Create a label for Alexa's personality messages.
status_label = Label(
    app_frame,
    text="Hello! Ready for some jokes?",
    font=("Courier", 10, "bold"),
    bg="#E8DDCC",
    fg="#40352C"
)

place_scaled(status_label, 40, 245, 680, 25)


# Create the label where the joke will appear.
joke_label = Label(
    app_frame,
    text="Your joke will appear here",
    font=("Courier", 12),
    bg="#E8DDCC",
    fg="#40352C",
    wraplength=650,
    justify=CENTER
)

place_scaled(joke_label, 35, 285, 690, 70)


#### Creating the main joke button

# Create the button that triggers a random joke.
joke_button = Button(
    app_frame,
    text="Alexa, tell me a joke",
    font=("Courier", 11, "bold"),
    bg="#B99A7C",
    fg="#FFFFFF",
    command=get_joke
)

place_scaled(joke_button, 155, 385, 450, 42)


#### Creating the request button

# Create the Tell me button.
request_button = Button(
    app_frame,
    text="Tell me.",
    font=("Courier", 11, "bold"),
    bg="#B99A7C",
    fg="white",
    command=show_punchline
)


#### Creating the laughing dialogue

# Create the laughing dialogue as a label.
laugh_label = Label(
    app_frame,
    text="Haha, get it?",
    font=("Courier", 12),
    bg="#E8DDCC",
    fg="#40352C"
)


#### Creating the joke rating buttons

# Create the rating prompt.
rating_prompt = Label(
    app_frame,
    text="So... how funny was that?",
    font=("Courier", 11, "bold"),
    bg="#E8DDCC",
    fg="#40352C"
)

# Create the first rating button.
rating1_button = Button(
    app_frame,
    text="Hilarious!",
    font=("Courier", 9, "bold"),
    bg="#A88A70",
    fg="#FFFFFF",
    command=lambda: rate_joke("Hilarious!")
)

# Create the second rating button.
rating2_button = Button(
    app_frame,
    text="It was okay.",
    font=("Courier", 9),
    bg="#A88A70",
    fg="#FFFFFF",
    command=lambda: rate_joke("It was okay.")
)

# Create the third rating button.
rating3_button = Button(
    app_frame,
    text="Never again!",
    font=("Courier", 9),
    bg="#A88A70",
    fg="#FFFFFF",
    command=lambda: rate_joke("Never again!")
)


#### Creating the session counter

# Create a label to display the number of jokes told.
counter_label = Label(
    app_frame,
    text="Jokes told: 0",
    font=("Courier", 10, "bold"),
    bg="#E8DDCC",
    fg="#40352C"
)

place_scaled(counter_label, 55, 170, 200, 25)


#### Creating Alexa's mood indicator

# Create a label to display Alexa's current mood.
mood_label = Label(
    app_frame,
    text="Mood: Happy",
    font=("Courier", 10, "bold"),
    bg="#E8DDCC",
    fg="#40352C"
)

place_scaled(mood_label, 505, 170, 200, 25)


#### Set the initial button visibility

# Hide the buttons that should only appear after a joke is selected.
request_button.place_forget()
laugh_label.place_forget()
question_button.place_forget()

rating_prompt.place_forget()
rating1_button.place_forget()
rating2_button.place_forget()
rating3_button.place_forget()


#### Activate responsive resizing

# Resize the interface whenever the main window changes size.
main.bind("<Configure>", resize_gui)


#### Run the application

# Keep the application running until the window is closed.
main.mainloop()