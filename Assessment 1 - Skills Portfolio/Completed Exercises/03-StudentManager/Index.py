from tkinter import *
import json
import os
from PIL import Image, ImageTk

# Set the base directory.
base_path = os.path.dirname(os.path.abspath(__file__))

# Set the file paths for the TXT and JSON files.
txt_path = os.path.join(base_path, "Assessment 1 - Skills Portfolio", "A1 - Resources", "studentMarks.txt")
json_path = os.path.join(base_path, "studentMarks.json")
image_path = os.path.join(base_path, "LOGO.png")

# Converts the original TXT file into a JSON database.
def convert_to_json():

    students = []

    # Open the original TXT file and read the student records.
    with open(txt_path, "r") as file:
        number_of_students = int(file.readline())

        for line in file:
            data = line.strip().split(",")

            # Store each student's information in a dictionary.
            student = {
                "studentNumber": int(data[0]),
                "name": data[1],
                "coursework1": int(data[2]),
                "coursework2": int(data[3]),
                "coursework3": int(data[4]),
                "examMark": int(data[5])
            }

            students.append(student)

    # Save all student records into the JSON database.
    with open(json_path, "w") as file:
        json.dump(students, file, indent = 4)

# Converts the TXT file into JSON (run only once).
# convert_to_json()

# Loads student records from the JSON database.
def load_students():

    with open(json_path, "r") as file:
        students = json.load(file)

    return students

# Calculates each student's coursework total, percentage and grade.
def calculate_results(student):

    coursework_total = student["coursework1"] + student["coursework2"] + student["coursework3"]

    total_mark = coursework_total + student["examMark"]

    percentage = (total_mark / 160) * 100

    # Assign a grade based on the overall percentage.
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return coursework_total, percentage, grade

# Retrieves an individual student's results.
def display_student(student):

    coursework_total, percentage, grade = calculate_results(student)

    result = (
    f"Student Name: {student['name']}\n"
    f"Student Number: {student['studentNumber']}\n"
    f"Coursework Total: {coursework_total} / 60\n"
    f"Exam Mark: {student['examMark']} / 100\n"
    f"Overall Percentage: {round(percentage, 2)}%\n"
    f"Grade: {grade}\n"
    f"{'-' * 30}\n"
    )

    return result

# Retrieves all student records and the class summary.
def view_all_students():

    students = load_students()

    total_percentage = 0
    result = ""

    # Retrieve and combine each student's results.
    for student in students:
        result += display_student(student)
        coursework_total, percentage, grade = calculate_results(student)
        total_percentage += percentage

    # Calculate the class average percentage.
    average_percentage = total_percentage / len(students)

    result += "\nCLASS SUMMARY\n"
    result += f"Number of students: {len(students)}\n"
    result += f"Average percentage: {round(average_percentage, 2)}%\n"

    return result

# Retrieves an individual student's record using their student number.
def view_individual_student(student_number):

    students = load_students()

    # Search for the student using their student number.
    for student in students:
        if student["studentNumber"] == student_number:
            return display_student(student)

    # Display a message if no matching student is found.
    return "Student not found."

# Retrieves the student with the highest overall mark.
def show_highest_student():

    students = load_students()

    highest_student = students[0]

    # Compare each student's total mark.
    for student in students:
        if calculate_results(student)[0] + student["examMark"] > calculate_results(highest_student)[0] + highest_student["examMark"]:
            highest_student = student

    return display_student(highest_student)

# Retrieves the student with the lowest overall mark.
def show_lowest_student():

    students = load_students()

    lowest_student = students[0]

    # Compare each student's total mark.
    for student in students:
        if calculate_results(student)[0] + student["examMark"] < calculate_results(lowest_student)[0] + lowest_student["examMark"]:
            lowest_student = student

    return display_student(lowest_student)

# Searches for and displays an individual student's results.
def search_student():

    # Use the student number entered by the user.
    student_number = student_number_entry.get()

    # Check whether the input contains a valid number.
    if student_number.isdigit():

        # Retrieve the student's results.
        result = view_individual_student(int(student_number))

        # Display the student's results.
        result_label.config(text = result)

    else:
        result_label.config(text = "Please enter a valid student number.")

    # Clear the input field.
    student_number_entry.delete(0, END)


main = Tk()
main.title("Student Manager") # Set the window title.
main.geometry("650x500") # Set the window size.
main.configure(bg = "#FFF1DB") # Set the background colour.
main.resizable(False, False) # Prevent the user from resizing the window.

## Create the header frame.
header = Frame(
    main,
    bg = "#23314F",
    width = 650,
    height = 130
)
header.place(x = 0, y = 0)

## Display the application logo

# Open the image.
pic1 = Image.open(image_path)

# Resize the image to the required dimensions.
pic2 = pic1.resize((90, 90))

# Convert the image for Tkinter.
logo = ImageTk.PhotoImage(pic2)

# Load and Display the application logo.
imglabel = Label(
    main,
    image = logo,
    bg = "#FFF1DB")
imglabel.place(x = 17, y = 17)

# Display the application title.
title_label = Label(
    header,
    text = "STUDENT MANAGER",
    bg = "#23314F",
    fg = "#FFFFFF",
    font = ("Times New Roman", 36, "bold", "italic")
    )
title_label.place(x = 135, y = 35)

## Create the main menu buttons.

# Button to switch to the all student records frame.
btn_all = Button(
    main,
    text = "All Student Records",
    font = ("Times New Roman", 16, "bold"),
    command = lambda:all_students_frame.place(x = 0, y = 0)
)
btn_all.place(x = 25, y = 160, width = 290, height = 140)

# Button to switch to the individual student records frame.
btn_individual = Button(
    main,
    text = "Individual Student Records",
    font = ("Times New Roman", 16, "bold"),
    command = lambda: individual_frame.place(x = 0, y = 0)
)
btn_individual.place(x = 335, y = 160, width = 290, height = 140)

# Button to switch to the highest overall score frame.
btn_highest = Button(
    main,
    text = "Highest Overall Mark",
    font = ("Times New Roman", 16, "bold")
)
btn_highest.place(x = 25, y = 330, width = 290, height = 140)

# Button to switch to the lowest overall score frame.
btn_lowest = Button(
    main,
    text = "Lowest Overall Mark",
    font = ("Times New Roman", 16, "bold")
)
btn_lowest.place(x = 335, y = 330, width = 290, height = 140)

## Create the all student records frame.
all_students_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the frame title.
heading = Label(
    all_students_frame,
    text = "ALL STUDENT RECORDS",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)

# Create the body area for the student table.
body_frame = Frame(
    all_students_frame,
    bg = "#FFFFFF"
)
body_frame.place(x = 25, y = 95, width = 600, height = 290)

# Allow the table columns to expand evenly.
for column in range(6):
    body_frame.grid_columnconfigure(column, weight = 1)

# Create the table headings.
headings = ["Name", "Number", "Coursework", "Exam", "Percentage", "Grade"]

for column, heading_text in enumerate(headings):

    label = Label(
        body_frame,
        text = heading_text,
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "white"
    )
    label.grid(row = 0, column = column, sticky = "nsew", padx = 5, pady = 5)

students = load_students()
total_percentage = 0

for row, student in enumerate(students, start = 1):

    # Calculate the student's results.
    coursework_total, percentage, grade = calculate_results(student)
    total_percentage += percentage

    # Store the information to display.
    details = [
        student["name"],
        student["studentNumber"],
        f"{coursework_total} / 60",
        f"{student['examMark']} / 100",
        f"{percentage:.2f}%",
        grade
    ]

    # Display each piece of information in the table.
    for column, detail in enumerate(details):

        label = Label(
            body_frame,
            text = detail,
            font = ("Times New Roman", 10),
            bg = "white"
        )
        label.grid(row = row, column = column, sticky = "nsew", padx = 2, pady = 2)

# Calculate the number of students and class average.
number_of_students = len(students)
average_percentage = total_percentage / number_of_students

# Display the class summary.
summary_label = Label(
    all_students_frame,
    text = f"Number of students: {number_of_students}     Average percentage: {average_percentage:.2f}%",
    font = ("Times New Roman", 13, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
summary_label.place(x = 25, y = 398)

# Create the back button.
back_button = Button(
    all_students_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = all_students_frame.place_forget
)
back_button.place(x = 250, y = 445, width = 150, height = 35)

## Create the individual student records frame.
individual_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the frame title.
heading = Label(
    individual_frame,
    text = "INDIVIDUAL STUDENT RECORDS",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)

# Ask the user to enter a student number.
instruction_label = Label(
    individual_frame,
    text = "Enter Student Number: ",
    font = ("Times New Roman", 14, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
instruction_label.place(x = 120, y = 115)

# Create the student number input field.
student_number_entry = Entry(
    individual_frame,
    font = ("Times New Roman", 14),
    justify = "center"
)
student_number_entry.place(x = 350, y = 115, width = 180, height = 30)

# Create an area to display the student's results.
result_label = Label(
    individual_frame,
    text = "",
    font = ("Times New Roman", 13),
    bg = "#FFFFFF",
    fg = "#23314F",
    justify = "left",
    anchor = "w",
    padx = 15,
    pady = 15
)
result_label.place(x = 100, y = 215, width = 450, height = 180)

# Create the search button.
search_button = Button(
    individual_frame,
    text = "Find Student",
    font = ("Times New Roman", 12, "bold"),
    command = search_student
)
search_button.place(x = 100, y = 170, width = 150, height = 35)

# Create the back button.
back_button = Button(
    individual_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = individual_frame.place_forget
)
back_button.place(x = 250, y = 430, width = 150, height = 35)

main.mainloop()