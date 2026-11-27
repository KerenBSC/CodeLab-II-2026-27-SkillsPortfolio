# ---- IMPORT LIBRARIES ---- #

from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import random
import json
import os


# ---- FILE PATHS ---- #

basePath = os.path.dirname(os.path.abspath(__file__))

# Asset folders
assetsPath = os.path.join(basePath, "assets")
imagePath = os.path.join(assetsPath, "images")
audioPath = os.path.join(assetsPath, "audio")
sfxPath = os.path.join(audioPath, "sounds")

# Data folder
dataPath = os.path.join(basePath, "data")
os.makedirs(dataPath, exist_ok = True)

highScorePath = os.path.join(dataPath, "highScore.json")
logoPath = os.path.join(imagePath, "LOGO.ico")


# ---- AUDIO SETUP ---- #

# Use Windows sound effects when available.
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

# Use pygame for background music and adjustable sound effects.
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False


# ---- AUDIO SETTINGS ---- #

bg_music_volume = 0.5
sfx_volume = 0.5
sfx_cache = {}


# ---- AUDIO FUNCTIONS ---- #

def play_bg_music(filename):

    if not HAS_PYGAME:
        return

    try:
        for ext in [".mp3", ".wav", ".ogg"]:
            musicPath = os.path.join(audioPath, filename + ext)

            if os.path.exists(musicPath):
                pygame.mixer.music.load(musicPath)
                pygame.mixer.music.set_volume(bg_music_volume)
                pygame.mixer.music.play(-1)
                break

    except Exception:
        pass


def update_bg_volume(val):

    global bg_music_volume
    bg_music_volume = float(val) / 100.0

    if HAS_PYGAME:
        try:
            pygame.mixer.music.set_volume(bg_music_volume)
        except Exception:
            pass


def play_sound(effect_type):

    if sfx_volume <= 0:
        return

    soundPath = os.path.join(sfxPath, f"{effect_type}.wav")

    if not os.path.exists(soundPath):
        return

    # Use pygame for adjustable sound effects.
    if HAS_PYGAME:
        try:
            if effect_type not in sfx_cache:
                sfx_cache[effect_type] = pygame.mixer.Sound(soundPath)

            sound = sfx_cache[effect_type]
            sound.stop()
            sound.set_volume(sfx_volume)
            sound.play()
            return

        except Exception:
            pass

    # Fall back to winsound if pygame is unavailable.
    if HAS_SOUND:
        try:
            winsound.PlaySound(
                soundPath,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except Exception:
            pass


def update_sfx_volume(val):

    global sfx_volume
    sfx_volume = float(val) / 100.0


def preview_sfx_volume(val):

    update_sfx_volume(val)
    play_sound("sparkle")


# ---- QUIZ VARIABLES ---- #

score = 0
highScores = {"Easy": 0, "Moderate": 0, "Advanced": 0}
currentQuestion = 0
attempts = 0
totalQuestions = 10
streak = 0
hearts = 3
skipsLeft = 1
perfectRound = True
milestonesShown = []

minValue = 1
maxValue = 9
difficultyLevel = "Easy"

num1 = 0
num2 = 0
operation = "+"

messages = [
    "Amazing! You're on fire! \U0001F525",
    "Brilliant! Keep it up! \u2728",
    "Maths genius! \U0001F31F",
    "Perfect! You're unstoppable!",
    "Another one conquered! \U0001F380"
]

milestoneMessages = {
    25: "25% complete! You're getting started!",
    50: "Halfway there! Keep going!",
    75: "75% complete! Almost at the finish line!",
    100: "You did it! All questions completed!"
}


# ---- LOAD HIGH SCORES ---- #

try:
    with open(highScorePath, "r") as file:
        data = json.load(file)

        if isinstance(data, dict):

            # Load scores for each difficulty.
            for level in highScores:
                if level in data:
                    highScores[level] = data[level]

            # Support the previous single-score format.
            if "high_score" in data:
                highScores["Easy"] = data["high_score"]

except (FileNotFoundError, ValueError, KeyError):
    pass


def updateHighScore():

    current_high = highScores.get(difficultyLevel, 0)

    if score > current_high:
        highScores[difficultyLevel] = score

        with open(highScorePath, "w") as file:
            json.dump(highScores, file)


# ---- GENERAL FUNCTIONS ---- #

def switchToFrame(frame):

    frame.tkraise()


def returnToMain():

    play_sound("click")

    if messagebox.askyesno(
        "Main Screen",
        "Are you sure you want to return to the main screen?"
    ):
        play_bg_music("BGmusic")
        switchToFrame(main)


def playAgain():

    play_sound("click")

    if messagebox.askyesno(
        "Play Again",
        "Would you like to play another quiz?"
    ):
        startQuiz(minValue, maxValue, difficultyLevel)


def showHighScores():

    play_sound("sparkle")

    popup = Toplevel(root)
    popup.title("High Scores \U0001F3C6")
    popup.geometry("320x260")
    popup.resizable(0, 0)
    popup.config(bg = "#FFFFFF")

    try:
        popup.iconbitmap(logoPath)
    except Exception:
        pass

    popup.transient(root)
    popup.grab_set()

    Label(
        popup,
        text = "\U0001F3C6 HIGH SCORES \U0001F3C6",
        font = ("Courier", 14, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).pack(pady = 20)

    for level in ["Easy", "Moderate", "Advanced"]:

        hs = highScores.get(level, 0)

        Label(
            popup,
            text = f"{level} Mode: {hs}/100",
            font = ("Courier", 11, "bold"),
            fg = "#490005",
            bg = "#FFFFFF"
        ).pack(pady = 8)

    Button(
        popup,
        text = "Close",
        font = ("Courier", 10, "bold"),
        fg = "#490005",
        bg = "#E8F4E8",
        activebackground = "#D2E8D2",
        activeforeground = "#490005",
        relief = RAISED,
        bd = 2,
        cursor = "hand2",
        width = 10,
        command = lambda: [play_sound("click"), popup.destroy()]
    ).pack(pady = 15)


def showSettings():

    play_sound("click")

    popup = Toplevel(root)
    popup.title("Settings ⚙️")
    popup.geometry("360x310")
    popup.resizable(0, 0)
    popup.config(bg = "#FFFFFF")

    try:
        popup.iconbitmap(logoPath)
    except Exception:
        pass

    popup.transient(root)
    popup.grab_set()
    popup.grid_columnconfigure(0, weight = 1)

    Label(
        popup,
        text = "⚙️ AUDIO SETTINGS ⚙️",
        font = ("Courier", 13, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).grid(row = 0, column = 0, pady = (18, 15))

    # Background music volume
    Label(
        popup,
        text = "Background Music Volume",
        font = ("Courier", 9, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).grid(row = 1, column = 0, pady = (5, 0))

    bg_slider = Scale(
        popup,
        from_ = 0,
        to = 100,
        orient = HORIZONTAL,
        command = update_bg_volume,
        bg = "#FFFFFF",
        highlightbackground = "#FFFFFF",
        troughcolor = "#E8F4E8",
        length = 270,
        showvalue = True
    )
    bg_slider.set(int(bg_music_volume * 100))
    bg_slider.grid(row = 2, column = 0, pady = (0, 12))

    # Sound effects volume
    Label(
        popup,
        text = "Sound Effects Volume",
        font = ("Courier", 9, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).grid(row = 3, column = 0, pady = (2, 0))

    sfx_slider = Scale(
        popup,
        from_ = 0,
        to = 100,
        orient = HORIZONTAL,
        command = preview_sfx_volume,
        bg = "#FFFFFF",
        highlightbackground = "#FFFFFF",
        troughcolor = "#E8F4E8",
        length = 270,
        showvalue = True
    )
    sfx_slider.set(int(sfx_volume * 100))
    sfx_slider.grid(row = 4, column = 0, pady = (0, 12))

    Button(
        popup,
        text = "Close",
        font = ("Courier", 10, "bold"),
        fg = "#490005",
        bg = "#E8F4E8",
        activebackground = "#D2E8D2",
        activeforeground = "#490005",
        relief = RAISED,
        bd = 2,
        cursor = "hand2",
        width = 10,
        command = lambda: [play_sound("click"), popup.destroy()]
    ).grid(row = 5, column = 0, pady = (0, 12))


# ---- PROGRESS MILESTONES ---- #

def checkProgressMilestone():

    completed = currentQuestion + 1
    percentage = int(completed / totalQuestions * 100)

    for milestone in [25, 50, 75, 100]:

        if percentage >= milestone and milestone not in milestonesShown:
            milestonesShown.append(milestone)
            milestoneLabel.config(text = milestoneMessages[milestone])
            return

    milestoneLabel.config(text = "")


# ---- QUIZ FUNCTIONS ---- #

def displayProblem():

    global num1, num2, operation, attempts

    attempts = 0

    num1 = random.randint(minValue, maxValue)
    num2 = random.randint(minValue, maxValue)
    operation = random.choice(["+", "-"])

    # Keep Easy Mode subtraction answers non-negative.
    if difficultyLevel == "Easy" and operation == "-" and num2 > num1:
        num1, num2 = num2, num1

    questionNumberLabel.config(
        text = f"Question {currentQuestion + 1} of {totalQuestions}"
    )

    questionLabel.config(text = f"{num1} {operation} {num2} =")

    answer.config(state = NORMAL)
    answer.delete(0, END)

    feedbackLabel.config(text = "Enter your answer in the box!")
    milestoneLabel.config(text = "")

    progressBar["value"] = currentQuestion
    updateHUD()

    submitButton.config(
        text = "Submit",
        state = NORMAL,
        command = submitAnswer
    )

    skipButton.config(
        text = f"Skip ({skipsLeft})",
        state = NORMAL if skipsLeft > 0 else DISABLED
    )


def updateHUD():

    scoreLabel.config(text = f"Score: {score}")
    livesLabel.config(text = "Lives: " + "\u2665 " * hearts)
    streakLabel.config(text = f"Streak: x{streak}")

    skipButton.config(
        text = f"Skip ({skipsLeft})",
        state = NORMAL if skipsLeft > 0 else DISABLED
    )


def skipQuestion():

    global skipsLeft, streak, perfectRound

    if skipsLeft > 0:

        play_sound("click")
        skipsLeft -= 1
        streak = 0
        perfectRound = False

        progressStatusLabels[currentQuestion].config(
            text = "\u21B7",
            fg = "#B8860B"
        )

        progressBar["value"] = currentQuestion + 1
        checkProgressMilestone()

        feedbackLabel.config(text = "Question skipped! Free skip used.")
        achievementLabel.config(text = "")

        answer.config(state = DISABLED)
        submitButton.config(text = "NEXT", command = nextQuestion)
        skipButton.config(state = DISABLED)

        updateHUD()

    else:
        play_sound("error")


def isCorrect(userAnswer):

    correctAnswer = num1 + num2 if operation == "+" else num1 - num2

    return userAnswer == correctAnswer


def submitAnswer():

    global score, attempts, streak, perfectRound, hearts

    # Check that the answer is a valid number.
    try:
        userAnswer = int(answer.get())
    except ValueError:
        play_sound("error")
        feedbackLabel.config(text = "Please enter a number!")
        return

    # Correct answer
    if isCorrect(userAnswer):

        streak += 1

        if streak == 5 or streak % 3 == 0:
            play_sound("streak")
        else:
            play_sound("sparkle")

        points = 10 if attempts == 0 else 5
        score = min(100, score + points)

        feedback = random.choice(messages)

        # Add bonus points for streaks.
        if streak % 3 == 0:
            score = min(100, score + 5)
            feedback += f"\n(+{points} marks!) \U0001F525 3 in a row (+5)!"
        elif streak == 5:
            score = min(100, score + 10)
            feedback += f"\n(+{points} marks!) \U0001F3C6 ACE (+10)!"
        else:
            feedback += f"\n(+{points} marks!)"

        # Update achievements.
        if streak == 5:
            achievementLabel.config(text = "\U0001F3C6 ACE!")
        elif streak % 3 == 0:
            achievementLabel.config(text = "\U0001F3C5 TRIPLE STREAK!")

        progressStatusLabels[currentQuestion].config(
            text = "\u2713",
            fg = "#008000"
        )

        progressBar["value"] = currentQuestion + 1
        checkProgressMilestone()

        updateHUD()
        feedbackLabel.config(text = feedback)

        answer.config(state = DISABLED)
        submitButton.config(text = "NEXT", command = nextQuestion)
        skipButton.config(state = DISABLED)

    # Incorrect answer
    else:

        score = max(0, score - 5)
        streak = 0
        perfectRound = False

        achievementLabel.config(text = "")
        updateHUD()

        if attempts == 0:

            play_sound("aw_man")
            attempts += 1

            feedbackLabel.config(
                text = "Not quite! -5 marks.\nOne more chance!"
            )

            answer.delete(0, END)

        else:

            play_sound("aw_man")
            hearts -= 1

            progressStatusLabels[currentQuestion].config(
                text = "\u2717",
                fg = "#FF0000"
            )

            progressBar["value"] = currentQuestion + 1
            checkProgressMilestone()

            feedbackLabel.config(
                text = "Incorrect! -5 marks.\nBetter luck next time!"
            )

            answer.config(state = DISABLED)
            skipButton.config(state = DISABLED)

            updateHUD()

            if hearts == 0:
                showGameOver()
                return

            submitButton.config(text = "NEXT", command = nextQuestion)


def nextQuestion():

    global currentQuestion

    play_sound("click")
    currentQuestion += 1

    if currentQuestion < totalQuestions:
        displayProblem()
    else:
        finishQuiz()


# ---- START QUIZ ---- #

def startQuiz(minimum, maximum, level):

    global score, currentQuestion, attempts
    global streak, perfectRound, hearts, skipsLeft
    global minValue, maxValue, difficultyLevel, milestonesShown

    play_sound("diff_click")
    play_bg_music("GameRound")

    # Reset quiz progress.
    score = 0
    currentQuestion = 0
    attempts = 0
    streak = 0
    hearts = 3
    skipsLeft = 1
    perfectRound = True
    milestonesShown = []

    # Set the selected difficulty.
    minValue = minimum
    maxValue = maximum
    difficultyLevel = level

    # Reset the quiz display.
    livesLabel.config(text = "Lives: \u2665 \u2665 \u2665")
    scoreLabel.config(text = "Score: 0")
    streakLabel.config(text = "Streak: x0")
    achievementLabel.config(text = "")
    milestoneLabel.config(text = "")

    quizTitle.config(text = f"\U0001065A {level.upper()} MODE \U0001065A")
    quizBGLabel.config(image = backgrounds[level])

    for label in progressStatusLabels:
        label.config(text = "-", fg = "#490005")

    progressBar["value"] = 0

    switchToFrame(quiz)
    displayProblem()


# ---- RESULTS FUNCTIONS ---- #

def finishQuiz():

    answer.config(state = DISABLED)
    submitButton.config(state = DISABLED)
    skipButton.config(state = DISABLED)

    progressBar["value"] = totalQuestions
    milestoneLabel.config(text = "")

    # Save the completed score.
    updateHighScore()

    # Calculate the final grade.
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    # Choose the results screen.
    if perfectRound:

        play_sound("victory")
        victoryScore.config(text = f"{score}/100 - PERFECT ROUND!")
        switchToFrame(victory)

    else:

        play_sound("victory")

        if score >= 90:
            title = "MATHS LEGEND! \U0001F3C6"
        elif score >= 70:
            title = "Amazing Work! \u2728"
        elif score >= 50:
            title = "Good Effort! \U0001F337"
        else:
            title = "Keep Practising! \U0001F497"

        resultTitle.config(text = title)
        resultScore.config(text = f"You got {score}/100!")
        resultGrade.config(text = f"Your Grade: {grade}")

        switchToFrame(results)


def showGameOver():

    play_sound("gameover")

    answer.config(state = DISABLED)
    submitButton.config(state = DISABLED)
    skipButton.config(state = DISABLED)

    gameOverScore.config(text = f"Final Score: {score}/100")
    switchToFrame(gameOver)


# ---- MAIN WINDOW ---- #

root = Tk()
root.title("Maths Quiz \u208a\u02da \U0001F4C8 \u27e1\U0001F4CF\u2081 \u02da")
root.geometry("650x560")
root.resizable(0, 0)

try:
    root.iconbitmap(logoPath)
except Exception:
    pass


# ---- LOAD BACKGROUNDS ---- #

def loadImage(filename, size = (520, 460)):

    imageFile = os.path.join(imagePath, filename)

    return ImageTk.PhotoImage(
        Image.open(imageFile).resize(size)
    )


mainimg = loadImage("MainBG.jpg", (650, 560))
easyimg = loadImage("easyBG.jpg", (650, 560))
modimg = loadImage("modBG.jpg", (650, 560))
advimg = loadImage("advBG.png", (650, 560))
resultsimg = loadImage("resultsBG.png", (650, 560))

backgrounds = {
    "Easy": easyimg,
    "Moderate": modimg,
    "Advanced": advimg
}


# ---- MAIN MENU ---- #

main = Frame(root, width = 650, height = 560)
main.place(x = 0, y = 0, width = 650, height = 560)

mainBG = Label(main, image = mainimg)
mainBG.place(x = 0, y = 0, relwidth = 1, relheight = 1)


# ---- MAIN MENU TITLE ---- #

title = Label(
    main,
    text = "MATHS QUIZ",
    font = ("Courier", 30, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 15
)
title.place(x = 325, y = 67, anchor = "center")


# ---- HIGH SCORES & SETTINGS ---- #

highScoreButton = Button(
    main,
    text = "\U0001F3C6 High Scores",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    activebackground = "#FFF4D6",
    activeforeground = "#490005",
    relief = RAISED,
    bd = 2,
    cursor = "hand2",
    command = showHighScores
)
highScoreButton.place(x = 220, y = 495, anchor = "center", width = 145, height = 30)

settingsButton = Button(
    main,
    text = "⚙️ Settings",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    activebackground = "#FFF4D6",
    activeforeground = "#490005",
    relief = RAISED,
    bd = 2,
    cursor = "hand2",
    command = showSettings
)
settingsButton.place(x = 430, y = 495, anchor = "center", width = 145, height = 30)


# ---- DIFFICULTY MENU ---- #

menu = Frame(main, bg = "#FFFFFF", width = 500, height = 360)
menu.place(x = 325, y = 290, anchor = "center")

difficulty = Label(
    menu,
    text = "Difficulty Level",
    font = ("Courier", 24, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
difficulty.place(relx = 0.5, y = 45, anchor = "center")


# ---- DIFFICULTY BUTTONS ---- #

difficultyLevels = {
    "Easy": (1, 9),
    "Moderate": (10, 99),
    "Advanced": (1000, 9999)
}

difficultyStyles = {
    "Easy": {
        "buttonText": "\u273f  EASY  \u273f",
        "buttonColour": "#E8F4E8",
        "description": "Single-digit numbers | 1-9",
        "tagline": "A gentle warm-up. You've got this!"
    },
    "Moderate": {
        "buttonText": "\u2726  MODERATE  \u2726",
        "buttonColour": "#FFF0CC",
        "description": "Double-digit numbers | 10-99",
        "tagline": "A little challenge never hurt!"
    },
    "Advanced": {
        "buttonText": "\u265B  ADVANCED  \u265B",
        "buttonColour": "#F8DDE3",
        "description": "Four-digit numbers | 1,000-9,999",
        "tagline": "Big numbers. Bigger brain energy."
    }
}

for level, y in [
    ("Easy", 105),
    ("Moderate", 190),
    ("Advanced", 275)
]:

    style = difficultyStyles[level]
    minimum, maximum = difficultyLevels[level]

    Button(
        menu,
        text = style["buttonText"],
        font = ("Courier", 12, "bold"),
        fg = "#490005",
        bg = style["buttonColour"],
        activebackground = style["buttonColour"],
        activeforeground = "#490005",
        relief = RAISED,
        bd = 3,
        width = 22,
        cursor = "hand2",
        command = lambda l = level, mn = minimum, mx = maximum: startQuiz(mn, mx, l)
    ).place(relx = 0.5, y = y, anchor = "center")

    Label(
        menu,
        text = style["description"],
        font = ("Courier", 10, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).place(relx = 0.5, y = y + 24, anchor = "center")

    Label(
        menu,
        text = style["tagline"],
        font = ("Courier", 8, "italic"),
        fg = "#8B5A5A",
        bg = "#FFFFFF"
    ).place(relx = 0.5, y = y + 43, anchor = "center")


# ---- MAIN MENU TIP ---- #

tipLabel = Label(
    main,
    text = "TIP: Build a streak to earn bonus points!",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
tipLabel.place(relx = 0.5, y = 530, anchor = "center")


# ---- QUIZ SCREEN ---- #

quiz = Frame(root, width = 650, height = 560)
quiz.place(x = 0, y = 0, width = 650, height = 560)

quizBGLabel = Label(quiz, image = easyimg)
quizBGLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)


# ---- QUIZ TITLE ---- #

quizTitle = Label(
    quiz,
    text = "\U0001065A EASY MODE \U0001065A",
    font = ("Courier", 24, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
quizTitle.place(x = 30, y = 30, width = 591, height = 65)


# ---- PROGRESS PANEL ---- #

prog = Frame(quiz, bg = "#FFFFFF")
prog.place(x = 30, y = 115, width = 180, height = 390)

progTitle = Label(
    prog,
    text = "PROGRESS",
    font = ("Courier", 16, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
progTitle.place(relx = 0.5, y = 35, anchor = "center")

progressStatusLabels = []

for i in range(totalQuestions):

    Label(
        prog,
        text = f"Q{i + 1}",
        font = ("Courier", 10, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    ).place(x = 45, y = 65 + i * 24)

    indic = Label(
        prog,
        text = "-",
        font = ("Courier", 10, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    )
    indic.place(x = 115, y = 65 + i * 24)
    progressStatusLabels.append(indic)


homeButton = Button(
    prog,
    text = "HOME",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    command = returnToMain
)
homeButton.place(x = 45, y = 335, width = 90)


# ---- QUESTION AREA ---- #

area = Frame(quiz, bg = "#FFFFFF", bd = 0, highlightthickness = 0)
area.place(x = 235, y = 115, width = 385, height = 390)


# Score, lives and streak
scoreLabel = Label(
    area,
    text = "Score: 0",
    font = ("Courier", 10, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
scoreLabel.place(x = 20, y = 25, anchor = "w")

livesLabel = Label(
    area,
    text = "Lives: \u2665 \u2665 \u2665",
    font = ("Courier", 10, "bold"),
    fg = "#D32F2F",
    bg = "#FFFFFF"
)
livesLabel.place(x = 20, y = 50, anchor = "w")

streakLabel = Label(
    area,
    text = "Streak: x0",
    font = ("Courier", 10, "bold"),
    fg = "#E65100",
    bg = "#FFFFFF"
)
streakLabel.place(x = 365, y = 28, anchor = "e")

ttk.Separator(area, orient = "horizontal").place(x = 20, y = 72, width = 345)


# Achievement display
achievementLabel = Label(
    area,
    text = "",
    font = ("Courier", 8, "bold"),
    fg = "#8B5A00",
    bg = "#FFF4D6",
    relief = FLAT
)
achievementLabel.place(x = 20, y = 85, width = 345, height = 25)


# Question display
questionNumberLabel = Label(
    area,
    text = "Question 1 of 10",
    font = ("Courier", 9, "bold"),
    fg = "#8C6265",
    bg = "#FFFFFF"
)
questionNumberLabel.place(x = 20, y = 140, anchor = "w")

questionLabel = Label(
    area,
    text = "0 + 0 =",
    font = ("Courier", 22, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
questionLabel.place(x = 20, y = 172, anchor = "w")


# Answer input and controls
answer = Entry(
    area,
    font = ("Courier", 14, "bold"),
    fg = "#490005",
    bg = "#F8F9FA",
    justify = CENTER,
    relief = SOLID,
    bd = 1
)
answer.place(x = 20, y = 205, width = 155, height = 38)

submitButton = Button(
    area,
    text = "Submit",
    font = ("Courier", 10, "bold"),
    fg = "#FFFFFF",
    bg = "#490005",
    activebackground = "#6B141C",
    activeforeground = "#FFFFFF",
    relief = FLAT,
    cursor = "hand2",
    command = submitAnswer
)
submitButton.place(x = 190, y = 205, width = 85, height = 38)

skipButton = Button(
    area,
    text = "Skip (1)",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#FFF4D6",
    activebackground = "#FFE89D",
    activeforeground = "#490005",
    relief = FLAT,
    cursor = "hand2",
    command = skipQuestion
)
skipButton.place(x = 285, y = 205, width = 80, height = 38)


# Answer feedback
feedbackLabel = Label(
    area,
    text = "Enter your answer in the box!",
    font = ("Courier", 9, "bold"),
    fg = "#490005",
    bg = "#F8F9FA",
    justify = CENTER,
    wraplength = 335
)
feedbackLabel.place(x = 20, y = 265, width = 345, height = 52)


# Progress milestone
milestoneLabel = Label(
    area,
    text = "",
    font = ("Courier", 8, "bold"),
    fg = "#B8860B",
    bg = "#FFFFFF"
)
milestoneLabel.place(x = 20, y = 323, width = 345, height = 18)

progressBar = ttk.Progressbar(
    area,
    length = 345,
    maximum = totalQuestions,
    mode = "determinate"
)
progressBar.place(x = 20, y = 345)


# ---- RESULTS SCREEN ---- #

results = Frame(root, width = 650, height = 560)
results.place(x = 0, y = 0, width = 650, height = 560)

resultsBG = Label(results, image = resultsimg)
resultsBG.place(x = 0, y = 0, relwidth = 1, relheight = 1)

resultTitle = Label(
    results,
    text = "",
    font = ("Courier", 22, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultTitle.place(x = 25, y = 45, width = 600, height = 55)

resultGrade = Label(
    results,
    text = "",
    font = ("Courier", 18, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultGrade.place(x = 55, y = 180, width = 240, height = 55)

resultScore = Label(
    results,
    text = "",
    font = ("Courier", 15, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultScore.place(x = 355, y = 180, width = 240, height = 55)


# Results buttons
Button(
    results,
    text = "Play Again",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = playAgain
).place(x = 190, y = 390, anchor = "center")

Button(
    results,
    text = "Main Screen",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = returnToMain
).place(x = 460, y = 390, anchor = "center")


# ---- PERFECT ROUND SCREEN ---- #

victory = Frame(root, bg = "#FFF4D6")
victory.place(x = 0, y = 0, width = 650, height = 560)

victoryTitle = Label(
    victory,
    text = "YOU'RE A GENIUS!",
    font = ("Courier", 22, "bold"),
    fg = "#8B5A00",
    bg = "#FFF4D6"
)
victoryTitle.place(x = 25, y = 35, width = 600, height = 55)

trophyLabel = Label(
    victory,
    text = "\U0001F3C6",
    font = ("Arial", 55),
    bg = "#FFF4D6"
)
trophyLabel.place(x = 105, y = 165, width = 180, height = 120)

prizeLabel = Label(
    victory,
    text = "GOLDEN GENIUS AWARD UNLOCKED!",
    font = ("Courier", 11, "bold"),
    fg = "#8B5A00",
    bg = "#FFF4D6"
)
prizeLabel.place(x = 310, y = 175, width = 300, height = 55)

victoryScore = Label(
    victory,
    text = "10/10 - PERFECT ROUND!",
    font = ("Courier", 13, "bold"),
    fg = "#490005",
    bg = "#FFF4D6"
)
victoryScore.place(x = 310, y = 245, width = 300, height = 45)


# Victory buttons
Button(
    victory,
    text = "Play Again",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = playAgain
).place(x = 190, y = 400, anchor = "center")

Button(
    victory,
    text = "Main Screen",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = returnToMain
).place(x = 460, y = 400, anchor = "center")


# ---- GAME OVER SCREEN ---- #

gameOver = Frame(root, bg = "#FCE4E4")
gameOver.place(x = 0, y = 0, width = 650, height = 560)

Label(
    gameOver,
    text = "OUT OF HEARTS! \U0001F494",
    font = ("Courier", 22, "bold"),
    fg = "#490005",
    bg = "#FCE4E4"
).place(x = 25, y = 45, width = 600, height = 60)

Label(
    gameOver,
    text = "You've run out of lives!",
    font = ("Courier", 12),
    fg = "#490005",
    bg = "#FCE4E4"
).place(x = 55, y = 200, width = 240, height = 60)

gameOverScore = Label(
    gameOver,
    text = "Final Score: 0/100",
    font = ("Courier", 14, "bold"),
    fg = "#490005",
    bg = "#FCE4E4"
)
gameOverScore.place(x = 355, y = 200, width = 240, height = 60)

Button(
    gameOver,
    text = "TRY AGAIN",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    command = playAgain
).place(x = 190, y = 390, anchor = "center")

Button(
    gameOver,
    text = "MAIN SCREEN",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    command = returnToMain
).place(x = 460, y = 390, anchor = "center")


# ---- KEYBOARD CONTROLS ---- #

def enterKey(event):

    if quiz.winfo_ismapped():

        if str(submitButton["text"]).upper() == "NEXT":
            nextQuestion()

        elif str(submitButton["state"]) == "normal":
            submitAnswer()


root.bind("<Return>", enterKey)


# ---- RUN APPLICATION ---- #

play_bg_music("BGmusic")
switchToFrame(main)

root.mainloop()
