# ---- IMPORT LIBRARIES ---- #

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os


# ---- FILE PATHS ---- #

base_path = os.path.dirname(os.path.abspath(__file__))

images_path = os.path.join(base_path, "images")
music_path = os.path.join(base_path, "music")
sounds_path = os.path.join(base_path, "sfx")

jokes_path = os.path.join(
    base_path, "..", "..", "A1 - Resources", "randomJokes.txt"
)


# ---- AUDIO SETUP ---- #

# Install pygame to enable background music and adjustable audio volumes:
# python -m pip install pygame

bg_music_volume = 40
sfx_volume = 70
sound_cache = {}

# Check whether pygame is available.
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

# Check whether Windows sound effects are available.
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


# Use alternative effects if a sound file is missing.
sound_fallbacks = {
    "joke_request": "punchline",
    "fullscreen": "show_question",
    "laugh": "punchline",
    "exit": "secret"
}


def play_sound(name):
    """Play a sound effect at the selected volume."""

    if sfx_volume <= 0:
        return

    sound_file = os.path.join(sounds_path, name + ".wav")

    # Try an alternative sound if the requested file is missing.
    if not os.path.exists(sound_file):
        fallback = sound_fallbacks.get(name)

        if fallback is None:
            return

        sound_file = os.path.join(sounds_path, fallback + ".wav")
        name = fallback

    if not os.path.exists(sound_file):
        return

    # Play the sound using pygame.
    if HAS_PYGAME:
        try:
            if name not in sound_cache:
                sound_cache[name] = pygame.mixer.Sound(sound_file)

            sound = sound_cache[name]
            sound.set_volume(sfx_volume / 100)

            channel = pygame.mixer.Channel(1)
            channel.stop()
            channel.play(sound)
            return

        except Exception:
            pass

    # Use winsound if pygame is unavailable.
    if HAS_WINSOUND:
        try:
            winsound.PlaySound(
                sound_file,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except Exception:
            pass


def play_bg_music():
    """Start the background music and loop it continuously."""

    if not HAS_PYGAME:
        return

    # Check for either supported music format.
    music_file = os.path.join(music_path, "AlexaBGmusic.mp3")

    if not os.path.exists(music_file):
        music_file = os.path.join(music_path, "AlexaBGmusic.wav")

    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(bg_music_volume / 100)
            pygame.mixer.music.play(-1)
        except Exception:
            pass


def update_bg_volume(value):
    """Update the background music volume."""

    global bg_music_volume

    bg_music_volume = int(float(value))

    if HAS_PYGAME:
        try:
            pygame.mixer.music.set_volume(bg_music_volume / 100)
        except Exception:
            pass


def update_sfx_volume(value):
    """Update the sound effect volume and preview the setting."""

    global sfx_volume

    sfx_volume = int(float(value))
    play_sound("punchline")


# ---- MAIN WINDOW ---- #

main = Tk()
main.title("Alexa's Joke Corner")
main.geometry("760x590")
main.configure(bg = "#CBC0B6")
main.resizable(True, True)

# Load the application icon.
try:
    main.iconbitmap(os.path.join(images_path, "BooksLOGO.ico"))
except Exception:
    pass

app_frame = Frame(main, bg = "#CBC0B6")
app_frame.place(x = 0, y = 0, width = 760, height = 590)


# ---- WINDOW SIZE AND WIDGET POSITIONS ---- #

original_width = 760
original_height = 590

current_width = original_width
current_height = original_height

widget_positions = {}

background_original = None
mascot_originals = {}
mascot_images = {}

current_mood = "happy"
last_image_size = (original_width, original_height)


def place_scaled(widget, x, y, width, height):
    """Position a widget using the original window dimensions."""

    widget_positions[widget] = (x, y, width, height)

    scale_x = current_width / original_width
    scale_y = current_height / original_height

    widget.place(
        x = int(x * scale_x),
        y = int(y * scale_y),
        width = max(1, int(width * scale_x)),
        height = max(1, int(height * scale_y))
    )


def resize_gui(event):
    """Resize the widgets and images when the window changes size."""

    global current_width, current_height
    global bg_image, mascot_images, last_image_size

    if event.widget != main:
        return

    current_width = event.width
    current_height = event.height

    if current_width <= 0 or current_height <= 0:
        return

    app_frame.place(width = current_width, height = current_height)

    scale_x = current_width / original_width
    scale_y = current_height / original_height

    # Resize each widget according to the new window dimensions.
    for widget, position in widget_positions.items():

        if widget.winfo_manager() == "place":
            x, y, width, height = position

            widget.place(
                x = int(x * scale_x),
                y = int(y * scale_y),
                width = max(1, int(width * scale_x)),
                height = max(1, int(height * scale_y))
            )

            if widget == joke_label:
                widget.config(wraplength = max(1, int(650 * scale_x)))

    if last_image_size == (current_width, current_height):
        return

    # Resize the background image while keeping its proportions.
    bg_scale = max(scale_x, scale_y)

    bg_size = (
        int(original_width * bg_scale),
        int(original_height * bg_scale)
    )

    bg_image = ImageTk.PhotoImage(
        background_original.resize(bg_size, Image.LANCZOS)
    )

    background.config(image = bg_image)

    # Resize all mascot images.
    mascot_scale = min(scale_x, scale_y)
    mascot_images = {}

    for mood, original_image in mascot_originals.items():

        size = (
            max(1, int(160 * mascot_scale)),
            max(1, int(85 * mascot_scale))
        )

        mascot_images[mood] = ImageTk.PhotoImage(
            original_image.resize(size, Image.LANCZOS)
        )

    mascot_label.config(image = mascot_images[current_mood])

    last_image_size = (current_width, current_height)


# ---- FULLSCREEN CONTROLS ---- #

fullscreen = False


def toggle_fullscreen(button = None):
    """Switch between fullscreen and normal window mode."""

    global fullscreen

    play_sound("fullscreen")

    if not fullscreen:
        main.state("zoomed")
        fullscreen = True

        if button:
            button.config(text = "Exit Fullscreen")

    else:
        main.state("normal")

        x = (main.winfo_screenwidth() - 760) // 2
        y = (main.winfo_screenheight() - 590) // 2

        main.geometry(f"760x590+{x}+{y}")
        fullscreen = False

        if button:
            button.config(text = "Go Fullscreen")


def exit_fullscreen(event):
    """Exit fullscreen mode when Escape is pressed."""

    if fullscreen:
        toggle_fullscreen()


main.bind("<Escape>", exit_fullscreen)


# ---- SETTINGS WINDOW ---- #

def open_settings_popup():
    """Open the settings window for audio and fullscreen controls."""

    play_sound("joke_request")

    popup = Toplevel(main)
    popup.title("Settings")
    popup.geometry("320x300")
    popup.configure(bg = "#F5EBE6")
    popup.resizable(False, False)
    popup.transient(main)
    popup.grab_set()

    # Centre the settings window over the main application.
    x = main.winfo_x() + (main.winfo_width() - 320) // 2
    y = main.winfo_y() + (main.winfo_height() - 300) // 2

    popup.geometry(f"320x300+{x}+{y}")

    Label(
        popup,
        text = "SETTINGS",
        font = ("Courier", 12, "bold"),
        bg = "#F5EBE6",
        fg = "#40352C"
    ).pack(pady = (15, 10))

    # Background music volume control.
    Label(
        popup,
        text = "Background Music Volume",
        font = ("Courier", 9),
        bg = "#F5EBE6",
        fg = "#40352C"
    ).pack()

    bg_slider = Scale(
        popup,
        from_ = 0,
        to = 100,
        orient = HORIZONTAL,
        command = update_bg_volume,
        bg = "#F5EBE6",
        highlightbackground = "#F5EBE6"
    )

    bg_slider.set(bg_music_volume)
    bg_slider.pack(pady = (0, 10))

    # Sound effect volume control.
    Label(
        popup,
        text = "Sound Effects Volume",
        font = ("Courier", 9),
        bg = "#F5EBE6",
        fg = "#40352C"
    ).pack()

    sfx_slider = Scale(
        popup,
        from_ = 0,
        to = 100,
        orient = HORIZONTAL,
        command = update_sfx_volume,
        bg = "#F5EBE6",
        highlightbackground = "#F5EBE6"
    )

    sfx_slider.set(sfx_volume)
    sfx_slider.pack(pady = (0, 5))

    # Display an audio message depending on pygame availability.
    if not HAS_PYGAME:
        audio_message = (
            "Install pygame for adjustable audio:\n"
            "python -m pip install pygame"
        )
        audio_colour = "#8C3B32"

    else:
        audio_message = "Move the slider to preview the sound level."
        audio_colour = "#40352C"

    Label(
        popup,
        text = audio_message,
        font = ("Courier", 7),
        bg = "#F5EBE6",
        fg = audio_colour
    ).pack(pady = (0, 8))

    # Fullscreen control.
    fs_text = "Exit Fullscreen" if fullscreen else "Go Fullscreen"

    fs_button = Button(
        popup,
        text = fs_text,
        font = ("Courier", 9, "bold"),
        bg = "#8C6D53",
        fg = "#FFFFFF",
        activebackground = "#70543D",
        activeforeground = "#FFFFFF",
        cursor = "hand2",
        command = lambda: toggle_fullscreen(fs_button)
    )

    fs_button.pack(ipadx = 10, ipady = 3, pady = (0, 10))

    # Close the settings window.
    Button(
        popup,
        text = "Close",
        font = ("Courier", 9),
        bg = "#CBC0B6",
        fg = "#40352C",
        cursor = "hand2",
        command = popup.destroy
    ).pack(ipadx = 10)


# ---- LOAD JOKES ---- #

# Read jokes from the text file.
try:
    with open(jokes_path, "r", encoding = "utf-8") as joke_file:
        jokes = [line.strip() for line in joke_file if line.strip()]

# Use backup jokes if the file cannot be found.
except Exception:
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything?",
        "What do you call fake spaghetti? An impasta?",
        "Why did the scarecrow win an award? Because he was outstanding in his field?"
    ]


# ---- GAME VARIABLES ---- #

current_setup = ""
current_punchline = ""

jokes_told = 0
typing_job = None

title_clicks = 0
secret_unlocked = False

milestone_message = ""

# Messages displayed before revealing each joke.
setup_messages = [
    "I've got a good one for you!",
    "Prepare yourself. This one's funny!",
    "Okay, listen carefully...",
    "I think you're going to like this one!",
    "Another masterpiece coming right up!"
]

# Random reactions displayed after each punchline.
reactions = [
    "Haha, get it?",
    "I'm hilarious. I know.",
    "Don't laugh too hard!",
    "Okay, that one was questionable...",
    "You're welcome. I'm here all week!",
    "I really outdid myself there.",
    "HAHA! Get it? Get it?"
]


# ---- MASCOT MOOD ---- #

def set_mood(mood, display_text = None):
    """Update the mascot image, mood label and matching sound."""

    global current_mood

    current_mood = mood

    mood_label.config(
        text = display_text or "Mood: " + mood.capitalize()
    )

    mascot_label.config(image = mascot_images[mood])

    play_sound("mood_" + mood)


# ---- TYPEWRITER EFFECT ---- #

def type_text(text, index = 0, callback = None):
    """Display text one character at a time."""

    global typing_job

    if index <= len(text):
        joke_label.config(text = text[:index])

        typing_job = main.after(
            25,
            lambda: type_text(text, index + 1, callback)
        )

    else:
        typing_job = None

        if callback:
            callback()


def start_typing(text, callback = None):
    """Stop the previous typing effect before starting a new one."""

    global typing_job

    if typing_job is not None:
        main.after_cancel(typing_job)
        typing_job = None

    joke_label.config(text = "")

    type_text(text, 0, callback)


# ---- JOKE FUNCTIONS ---- #

def get_joke():
    """Choose a random joke and display its setup."""

    global current_setup, current_punchline
    global jokes_told, milestone_message

    play_sound("joke_request")

    # Separate the setup and punchline at the question mark.
    parts = random.choice(jokes).split("?", 1)

    current_setup = parts[0] + "?"
    current_punchline = parts[1].strip() if len(parts) > 1 else "Ha ha!"

    # Update the joke counter.
    jokes_told += 1
    counter_label.config(text = "Jokes told: " + str(jokes_told))

    # Display special messages at certain milestones.
    milestone_message = ""

    if jokes_told == 5:
        milestone_message = "5 jokes already! You're warming up!"

    elif jokes_told == 10:
        milestone_message = "10 jokes! You're officially a fan!"

    elif jokes_told == 20:
        milestone_message = "20 JOKES?! You're Alexa's biggest fan!"

    # Disable the main button until the current joke is finished.
    joke_button.config(
        text = "Alexa, tell me another joke",
        state = DISABLED
    )

    # Hide buttons and labels from the previous joke.
    for widget in (
        request_button,
        question_button,
        rating_prompt,
        rating1_button,
        rating2_button,
        rating3_button,
        laugh_label
    ):
        widget.place_forget()

    status_label.config(
        text = "Hmm... let me think of something funny."
    )

    set_mood("thinking")
    joke_label.config(text = "")

    main.after(
        900,
        lambda: start_typing(current_setup, setup_finished)
    )


def setup_finished():
    """Display a message and allow the user to reveal the punchline."""

    joke_button.config(state = NORMAL)

    status_label.config(
        text = milestone_message or random.choice(setup_messages)
    )

    set_mood("mischievous")

    place_scaled(request_button, 325, 445, 110, 35)


def show_punchline():
    """Display the punchline and prepare the rating buttons."""

    play_sound("punchline")

    # Hide buttons that are no longer needed.
    for widget in (
        request_button,
        rating_prompt,
        rating1_button,
        rating2_button,
        rating3_button
    ):
        widget.place_forget()

    question_button.config(state = DISABLED)

    status_label.config(text = "And here comes the best part...")

    set_mood("amused")

    start_typing(current_punchline, punchline_finished)


def punchline_finished():
    """Display Alexa's reaction and the joke rating options."""

    play_sound("laugh")

    laugh_label.config(text = random.choice(reactions))

    place_scaled(laugh_label, 200, 445, 360, 35)
    place_scaled(rating_prompt, 230, 495, 300, 25)

    # Display the three rating buttons.
    place_scaled(rating1_button, 55, 535, 180, 35)
    place_scaled(rating2_button, 290, 535, 180, 35)
    place_scaled(rating3_button, 525, 535, 180, 35)

    question_button.config(
        text = "Show Question",
        command = show_question,
        state = NORMAL
    )

    place_scaled(question_button, 590, 10, 130, 35)


def show_question():
    """Display the joke setup again."""

    play_sound("show_question")

    question_button.config(state = DISABLED)

    # Hide the reaction and rating options.
    for widget in (
        laugh_label,
        rating_prompt,
        rating1_button,
        rating2_button,
        rating3_button
    ):
        widget.place_forget()

    status_label.config(text = "Here's the question again!")

    set_mood("curious")

    start_typing(current_setup, question_finished)


def question_finished():
    """Restore the buttons for revealing the punchline."""

    question_button.config(
        text = "Show Joke",
        command = show_punchline,
        state = NORMAL
    )

    place_scaled(question_button, 590, 10, 130, 35)
    place_scaled(request_button, 325, 445, 110, 35)


# ---- JOKE RATINGS ---- #

def rate_joke(rating):
    """Display a response and play the matching rating sound."""

    responses = {
        "Hilarious!": (
            "I KNEW you'd like that one!",
            "rating_hilarious"
        ),
        "It was okay.": (
            "I'll try harder next time...",
            "rating_okay"
        ),
        "Never again!": (
            "Ouch. That hurt my feelings.",
            "rating_bad"
        )
    }

    response, sound = responses[rating]

    laugh_label.config(text = response)

    play_sound(sound)
    set_mood("happy", "Mood: " + rating)


# ---- SECRET MESSAGE AND EXIT ---- #

def secret_interaction(event):
    """Unlock a hidden message when the title is clicked five times."""

    global title_clicks, secret_unlocked

    if secret_unlocked:
        return

    title_clicks += 1

    if title_clicks == 5:
        secret_unlocked = True

        play_sound("secret")

        messagebox.showinfo(
            "Secret Unlocked!",
            "Congratulations!\n\n"
            "You've discovered my secret.\n"
            "Please don't tell anyone..."
        )


def confirm_exit():
    """Ask the user to confirm before closing the application."""

    if messagebox.askyesno("Exit?", "Confirm exit?"):

        play_sound("exit")

        # Stop the background music before closing.
        if HAS_PYGAME:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

        main.destroy()


# ---- LOAD BACKGROUND AND MASCOT IMAGES ---- #

# Load the background image or use a plain background if unavailable.
try:
    background_original = Image.open(
        os.path.join(images_path, "JokeBG.jpg")
    )

except Exception:
    background_original = Image.new("RGB", (760, 590), "#CBC0B6")


bg_image = ImageTk.PhotoImage(
    background_original.resize((760, 590), Image.LANCZOS)
)

background = Label(app_frame, image = bg_image)
place_scaled(background, 0, 0, 760, 590)


# Match each mascot mood to its image file.
mood_files = {
    "happy": "happy.jpg",
    "amused": "amused.jpg",
    "curious": "curious.jpg",
    "mischievous": "mischievous.jpg",
    "thinking": "thinking.jpg"
}


# Load and resize the mascot images.
for mood, filename in mood_files.items():

    try:
        mascot_originals[mood] = Image.open(
            os.path.join(images_path, filename)
        )

    except Exception:
        mascot_originals[mood] = Image.new(
            "RGB", (160, 85), "#E8DDCC"
        )

    mascot_images[mood] = ImageTk.PhotoImage(
        mascot_originals[mood].resize((160, 85), Image.LANCZOS)
    )


# ---- TOP BUTTONS AND TITLE ---- #

# Exit button.
exit_button = Button(
    app_frame,
    text = "Exit",
    font = ("Courier", 10, "bold"),
    bg = "#8C6D53",
    fg = "#FFFFFF",
    activebackground = "#70543D",
    activeforeground = "#FFFFFF",
    relief = RAISED,
    bd = 2,
    cursor = "hand2",
    command = confirm_exit
)

place_scaled(exit_button, 40, 10, 130, 35)


# Settings button.
settings_button = Button(
    app_frame,
    text = "⚙",
    font = ("Courier", 11, "bold"),
    bg = "#8C6D53",
    fg = "#FFFFFF",
    activebackground = "#70543D",
    activeforeground = "#FFFFFF",
    relief = RAISED,
    bd = 2,
    cursor = "hand2",
    command = open_settings_popup
)

place_scaled(settings_button, 360, 10, 40, 35)


# Button for showing the joke question.
question_button = Button(
    app_frame,
    text = "Show Question",
    font = ("Georgia", 10, "bold"),
    bg = "#8C6D53",
    fg = "#FFFFFF",
    relief = RAISED,
    bd = 2,
    cursor = "hand2"
)


# Application title. Clicking it five times unlocks a secret message.
title_label = Label(
    app_frame,
    text = "Alexa's Joke Corner",
    font = ("Courier", 18, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C",
    relief = GROOVE,
    bd = 2
)

place_scaled(title_label, 40, 65, 680, 55)
title_label.bind("<Button-1>", secret_interaction)


# ---- MASCOT AND STATUS LABELS ---- #

# Mascot image.
mascot_label = Label(
    app_frame,
    image = mascot_images["happy"],
    bg = "#F5EBE6",
    relief = SOLID,
    bd = 1
)

place_scaled(mascot_label, 300, 140, 160, 85)


# Joke counter.
counter_label = Label(
    app_frame,
    text = "Jokes told: 0",
    font = ("Courier", 10, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C"
)

place_scaled(counter_label, 55, 170, 200, 25)


# Current mascot mood.
mood_label = Label(
    app_frame,
    text = "Mood: Happy",
    font = ("Courier", 10, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C"
)

place_scaled(mood_label, 505, 170, 200, 25)


# Status message displayed throughout the application.
status_label = Label(
    app_frame,
    text = "Hello! Ready for some jokes?",
    font = ("Courier", 10, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C"
)

place_scaled(status_label, 40, 245, 680, 25)


# Main area for displaying the joke.
joke_label = Label(
    app_frame,
    text = "Your joke will appear here",
    font = ("Courier", 12, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C",
    wraplength = 650,
    justify = CENTER,
    relief = SOLID,
    bd = 1
)

place_scaled(joke_label, 35, 285, 690, 70)


# ---- JOKE AND RATING BUTTONS ---- #

# Main button for requesting a joke.
joke_button = Button(
    app_frame,
    text = "Alexa, tell me a joke",
    font = ("Courier", 11, "bold"),
    bg = "#A37C5D",
    fg = "#FFFFFF",
    activebackground = "#846247",
    activeforeground = "#FFFFFF",
    relief = RAISED,
    bd = 3,
    cursor = "hand2",
    command = get_joke
)

place_scaled(joke_button, 155, 385, 450, 42)


# Button for revealing the punchline.
request_button = Button(
    app_frame,
    text = "Tell me.",
    font = ("Courier", 11, "bold"),
    bg = "#A37C5D",
    fg = "white",
    relief = RAISED,
    cursor = "hand2",
    command = show_punchline
)


# Alexa's reaction after the punchline.
laugh_label = Label(
    app_frame,
    text = "Haha, get it?",
    font = ("Courier", 12, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C"
)


# Prompt asking the user to rate the joke.
rating_prompt = Label(
    app_frame,
    text = "So... how funny was that?",
    font = ("Courier", 11, "bold"),
    bg = "#F5EBE6",
    fg = "#40352C"
)


# Three buttons for rating the joke.
rating_buttons = [
    Button(
        app_frame,
        text = "Hilarious!",
        font = ("Courier", 9, "bold"),
        bg = "#8C6D53",
        fg = "#FFFFFF",
        cursor = "hand2",
        command = lambda: rate_joke("Hilarious!")
    ),

    Button(
        app_frame,
        text = "It was okay.",
        font = ("Courier", 9, "bold"),
        bg = "#8C6D53",
        fg = "#FFFFFF",
        cursor = "hand2",
        command = lambda: rate_joke("It was okay.")
    ),

    Button(
        app_frame,
        text = "Never again!",
        font = ("Courier", 9, "bold"),
        bg = "#8C6D53",
        fg = "#FFFFFF",
        cursor = "hand2",
        command = lambda: rate_joke("Never again!")
    )
]

rating1_button, rating2_button, rating3_button = rating_buttons


# ---- INITIAL BUTTON VISIBILITY ---- #

# Hide buttons and labels until they are needed.
for widget in (
    request_button,
    question_button,
    laugh_label,
    rating_prompt,
    rating1_button,
    rating2_button,
    rating3_button
):
    widget.place_forget()


# ---- START THE APPLICATION ---- #

# Connect the window resizing event and start the background music.
main.bind("<Configure>", resize_gui)

play_bg_music()

main.mainloop()