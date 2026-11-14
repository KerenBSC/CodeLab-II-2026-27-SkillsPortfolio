# Import the libraries needed for the quiz.
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import os

# Set the working directory to the folder containing this Python file.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---- Functions ---- #

# Switch between the different pages of the application.
def switch_to_frame(frame):
    frame.tkraise()

# Generate a random number within the given range.
def randomInt(minValue, maxValue):
    return random.randint(minValue, maxValue)

# Randomly choose addition or subtraction.
def decideOperation():
    return random.choice(["+", "-"])

# ---- Quiz Variables ---- #

# Keep track of the player's score and quiz progress.
score = 0
currentQuestion = 0
attempts = 0
totalQuestions = 10

# Store the current difficulty settings.
minValue = 1
maxValue = 9
difficultyLevel = "Easy"
currentBackground = None

# ---- Quiz Functions ---- #

# Generate and display a new maths question.
def displayProblem():
    global num1, num2, operation, attempts

    # Reset the number of attempts for the new question.
    attempts = 0

    # Generate two random numbers and choose an operation.
    num1 = randomInt(minValue, maxValue)
    num2 = randomInt(minValue, maxValue)
    operation = decideOperation()

    # Prevent negative answers in Easy Mode.
    if difficultyLevel == "Easy" and operation == '-' and num2 > num1:
        num1, num2 = num2, num1

    # Update the question number and question display.
    questionNumberLabel.config(
        text = f"Question {currentQuestion + 1}"
    )

    questionLabel.config(
        text = f"{num1} {operation} {num2} ="
    )

    # Clear the previous answer and feedback.
    answer.config(state = NORMAL)
    answer.delete(0, END)
    feedbackLabel.config(text = "")

    # Reset the submit button for the new question.
    submitButton.config(
        text = "Submit",
        state = NORMAL,
        command = submitAnswer
    )

# Check whether the user's answer is correct
def isCorrect(userAnswer):

    # Calculate the correct answer based on the operation.
    if operation == "+":
        correctAnswer = num1 + num2
    else:
        correctAnswer = num1 - num2

    return userAnswer == correctAnswer

# Check the player's answer and update the score.
def submitAnswer ():
    global score, attempts

    # Check that the answer entered is a valid number.
    try:
        userAnswer = int(answer.get())
    except ValueError:
        feedbackLabel.config(text = "Please enter a number!")
        return

    # Check whether the answer is correct.
    if isCorrect(userAnswer):

         # Award more points for answering correctly on the first attempt.
        if attempts == 0:
            score += 10
            feedbackLabel.config(text = "Correct!\nYou've earned 10 points!")
        else:
            score += 5
            feedbackLabel.config(text = "Correct!\nYou've earned 5 points!")

        # Mark the question as correct.
        progressStatusLabels[currentQuestion].config(text = "\u2713") # Unicode for the tick mark.

        # Update the score display.
        scoreLabel.config(text = f"Score: {score}")

        # Prevent the player from answering the same question again.
        answer.config(state = DISABLED)

        # Change the button to move to the next question.
        submitButton.config(
            text = "NEXT",
            command = nextQuestion
        )

    # Allow one more attempt if the first answer is incorrect.
    elif attempts == 0:
        attempts += 1
        feedbackLabel.config(text="Incorrect! Try again.")
        answer.delete(0, END)

    # If the second attempt is also incorrect, move on.
    else:
        feedbackLabel.config(text="Incorrect! No points.")

        # Mark the question as incorrect.
        progressStatusLabels[currentQuestion].config(text="\u2717") # Unicode for the Ballot X.

        answer.config(state=DISABLED)
        submitButton.config(
            text="Next",
            command=nextQuestion
        )

# Move to the next question or finish the quiz.
def nextQuestion():
    global currentQuestion

    currentQuestion += 1

    if currentQuestion < totalQuestions:
        displayProblem()

    else:
        finishQuiz()

# ---- Results function ---- #

# Calculate and display the player's final results.
def finishQuiz():

    # Disable the answer box and submit button.
    answer.config(state = DISABLED)
    submitButton.config(state = DISABLED)

    # Display a heading based on the final score.
    if score < 50:
        resultTitle.config(text="Aw man :(")
    else:
        resultTitle.config(text="Congratulations!")

    # Display the final score out of 100.
    resultScore.config(
        text=f"You got {score}/100!"
    )

    # Determine the player's grade.
    if score > 90:
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

    # Display the final grade.
    resultGrade.config(
        text=f"Your Grade: {grade}"
    )

    # Switch to the results page.
    switch_to_frame(results)

# Start a new quiz using the selected difficulty settings.
def startQuiz(minimum, maximum, level, background):
    global score, currentQuestion, attempts
    global minValue, maxValue, difficultyLevel, currentBackground

    # Reset the quiz variables.
    score = 0
    currentQuestion = 0
    attempts = 0

    # Update the selected difficulty settings.
    minValue = minimum
    maxValue = maximum
    difficultyLevel = level
    currentBackground = background

    # Update the quiz background and heading.
    quizBGLabel.config(image = background)
    quizTitle.config(text=f"𐙚 {level.upper()} MODE 𐙚")

    # Reset the score and progress indicators.
    scoreLabel.config(text="Score: 0")

    for label in progressStatusLabels:
        label.config(text="-")

    # Display the quiz page and generate the first question.
    switch_to_frame(quiz)
    displayProblem()

# Return to the main difficulty selection screen.
def returnToMain():

    # Ask the player to confirm before leaving the quiz.
    confirm = messagebox.askyesno(
        "Main Screen",
        "Are you sure you want to return to the main screen?"
    )

    if confirm:
        switch_to_frame(main)

# Allow the player to restart the quiz using the same difficulty.
def playAgain():

    # Ask the player whether they want to play again.
    confirm = messagebox.askyesno(
        "Play Again",
        "Would you like to play another quiz?"
    )

    if confirm:
        startQuiz(
            minValue,
            maxValue,
            difficultyLevel,
            currentBackground
        )

# ---- Main Window ---- #

# Create the main application window.
root = Tk()

# This window requires a title. Create a title in the output.
root.title('Maths Quiz ₊˚ 📈 ⟡📏｡ ˚')

# Creates an output window of size 400x335px.
root.geometry('400x335')

# Output Window Size is fixed
root.resizable(0, 0)

# Asign a new .ico file to the window to change it's icon.
root.iconbitmap('LOGO.ico')

# ---- Difficulty Menu ---- #

# Create the main menu frame.
main = Frame(root)
main.place(width = 400, height = 335)

# Load and display the main menu background.
img = ImageTk.PhotoImage(Image.open("MainBG.jpg"))
imgLabel = Label(main, image=img)
imgLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Display the main menu heading.
title = Label(
    main,
    text="MATHS QUIZ",
    font=("Courier", 28, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 11
)
title.place(x = 200, y = 50.5, anchor = "center")

# Create the panel containing the difficulty options.
menu = Frame(
    main,
    bg = "#FFFFFF",
    width = 345,
    height = 215
)
menu.place(x = 200, y = 202, anchor = "center")

# Display the difficulty selection heading.
difficulty = Label(
    menu,
    text = "Difficulty Level",
    font = ("Courier", 18, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
difficulty.place(x = 172.5, y = 37, anchor = "center")

# ---- Difficulty buttons ---- #

# Each button starts the quiz with its selected difficulty.
easyButton = Button(
    menu,
    text = "Easy",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: startQuiz(1, 9, "Easy", easyimg)
)
easyButton.place(x = 172.5, y = 87, anchor = "center")

modButton = Button(
    menu,
    text = "Moderate",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: startQuiz(10, 99, "Moderate", modimg)
)
modButton.place(x = 172.5, y = 128, anchor = "center")

advButton = Button(
    menu,
    text = "Advanced",
    font = ("Courier", 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 10,
    command = lambda: startQuiz(1000, 9999, "Advanced", advimg)
)
advButton.place(x = 172.5, y = 170, anchor = "center")

# ---- Quiz Backgrounds ---- #

# Load the backgrounds for each difficulty level.
easyimg = ImageTk.PhotoImage(Image.open("easyBG.jpg"))
modimg = ImageTk.PhotoImage(Image.open("modBG.jpg"))
advimg = ImageTk.PhotoImage(Image.open("advBG.png"))

# ---- Quiz frame (page) ---- #

# Frames are techincally different pages to the application
# Create one shared quiz frame for all difficulty levels.
quiz = Frame(root)
quiz.place(width = 400, height = 335)

# Display the quiz background.
quizBGLabel = Label(quiz, image = easyimg)
quizBGLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Display the quiz heading.
quizTitle = Label(
    quiz,
    text = "𐙚 EASY MODE 𐙚",
    font = ("Courier", 20, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
quizTitle.place(x = 154, y = 25, width = 228, height = 50)

# ---- Quiz Progress Panel ---- #

# Create a panel to display the progress of all 10 questions.
prog = Frame(
    quiz,
    bg = "#FFFFFF"
)
prog.place(x = 19, y = 24, width = 124, height = 289)

# Display the progress panel heading.
progTitle = Label(
    prog,
    text = "PROGRESS",
    font = ('Courier', 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
progTitle.place(x = 20, y = 10)

# Labels for the question numbers and their status.
progressLabels = []
progressStatusLabels = []

for i in range(10):

    # Display the question number.
    progress = Label(
        prog,
        text = f"Q{i + 1}",
        font = ('Courier', 12, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    )

    # Display the question status.
    indic = Label(
        prog,
        text = f"-",
        font = ('Courier', 12, "bold"),
        fg = "#490005",
        bg = "#FFFFFF"
    )

    # Position both labels inside the progress panel.
    progress.place(x = 30, y = 40 + (i * 23))
    indic.place(x = 75, y = 40 + (i * 23))

    # Store the labels so their text can be updated later.
    progressLabels.append(progress)
    progressStatusLabels.append(indic)

# ---- Question Area ---- #

# Create the area containing the question and answer widgets.
area = Frame(
    quiz,
    bg = "#FFFFFF",
)
area.place(x = 154, y = 83, width = 228, height = 230)

# Display the player's current score.
scoreLabel = Label(
    area,
    text="Score: 0",
    font=('Courier', 11, "bold"),
    fg="#490005",
    bg="#FFFFFF"
)
scoreLabel.place(x = 15, y = 15, width = 202)

# Display the current question number.
questionNumberLabel = Label(
    area,
    text = "",
    font = ('Courier', 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
questionNumberLabel.place(x = 20, y = 45, width = 100)

# Display the maths question.
questionLabel = Label(
    area,
    text = "",
    font = ('Courier', 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
questionLabel.place(x = -30, y = 70, width = 200)

# Create an entry box for the player's answer.
answer = Entry(
    area,
    font = ('Courier', 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    justify = CENTER,
    width = 12
)
answer.place(x = 25, y = 95)

# Create the button used to submit answers and move to the next question.
submitButton = Button(
    area,
    text = "Submit",
    font = ('Courier', 12, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    command = submitAnswer
)
submitButton.place(x = 20, y = 130)

# Display feedback after the player submits an answer.
feedbackLabel = Label(
    area,
    text = "",
    font = ('Courier', 9, "bold"),
    fg = "#490005",
    bg = "#FFFFFF"
)
feedbackLabel.place(x = 10, y = 175, width = 202, height = 45)

# ---- Results Page ---- #

# Create the frame for the final results.
results = Frame(root)
results.place(width = 400, height = 335)

# Load and display the results background.
resultsimg = ImageTk.PhotoImage(Image.open("resultsBG.png"))

resultsBG = Label(
    results,
    image = resultsimg
)
resultsBG.place(x=0, y=0, relwidth=1, relheight=1)

# Display the final results heading.
resultTitle = Label(
    results,
    text = "",
    font = ('Courier', 22, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultTitle.place(x = 200, y = 90, anchor = "center")

# Display the player's final grade.
resultGrade = Label(
    results,
    text = "",
    font = ('Courier', 18, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultGrade.place(x = 200, y = 150, anchor = "center")

# Display the player's final score.
resultScore = Label(
    results,
    text = "",
    font = ('Courier', 15, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    padx = 15
)
resultScore.place(x = 200, y = 185, anchor = "center")

# ---- Result Buttons ---- #

# Button to start another quiz.
againButton = Button(
    results,
    text = "Play Again",
    font = ("Courier", 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = playAgain
)
againButton.place(x = 115, y = 255, anchor = "center")

# Button to return to the main difficulty menu.
mainButton = Button(
    results,
    text = "Main screen",
    font = ('Courier', 11, "bold"),
    fg = "#490005",
    bg = "#FFFFFF",
    width = 12,
    command = returnToMain
)
mainButton.place(x = 285, y = 255, anchor = "center")

# ---- Run The Application ---- #

# Display the main menu when the application first opens.
switch_to_frame(main)

# Keep the application running until the window is closed.
root.mainloop()