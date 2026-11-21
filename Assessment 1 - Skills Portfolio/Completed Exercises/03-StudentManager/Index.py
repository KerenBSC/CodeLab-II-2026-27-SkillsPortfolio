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
rankimage_path = os.path.join(base_path, "HighestRank.png")

# Converts the original TXT file into a JSON database.
def convert_to_json():

    students = []

    # Open the original TXT file and read the student records.
    with open(txt_path, "r") as file:
        file.readline()

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

    return highest_student

# Retrieves the student with the lowest overall mark.
def show_lowest_student():

    students = load_students()

    lowest_student = students[0]

    # Compare each student's total mark.
    for student in students:
        if calculate_results(student)[0] + student["examMark"] < calculate_results(lowest_student)[0] + lowest_student["examMark"]:
            lowest_student = student

    return lowest_student

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

# Returns to the main menu and clears the previous search.
def back_to_individual_menu():

    individual_frame.place_forget()
    result_label.config(text = "")
    student_number_entry.delete(0, END)

# Opens the student records page for the selected action.
def open_records(action):

    global record_action

    record_action = action

    # Show sorting controls only for menu item 5.
    if record_action == "sort":
        sort_frame.place(x = 25, y = 90, width = 600, height = 45)
    else:
        sort_frame.place_forget()

    # Refresh the table before displaying the page.
    refresh_student_table()

    all_students_frame.place(x = 0, y = 0)


# Sorts student records according to the selected category and order.
def apply_sort():

    students = load_students()

    # Sort records alphabetically by student name.
    if sort_by_var.get() == "Name":
        students.sort(key = lambda student: student["name"].lower())

    # Sort records numerically by student number.
    elif sort_by_var.get() == "Student Number":
        students.sort(key = lambda student: student["studentNumber"])

    # Sort records by coursework total.
    elif sort_by_var.get() == "Coursework Total":
        students.sort(key = lambda student: calculate_results(student)[0])

    # Sort records by exam mark.
    elif sort_by_var.get() == "Exam Mark":
        students.sort(key = lambda student: student["examMark"])

    # Sort records by overall percentage.
    elif sort_by_var.get() == "Overall Percentage":
        students.sort(key = lambda student: calculate_results(student)[1])

    # Sort records alphabetically by grade.
    elif sort_by_var.get() == "Grade":
        students.sort(key = lambda student: calculate_results(student)[2])

    # Reverse the order if descending is selected.
    if sort_order_var.get() == "Descending":
        students.reverse()

    # Refresh the table using the sorted records.
    refresh_student_table(students)

# Resets the sorting options and restores the original record order.
def reset_sort():

    sort_by_var.set("Name")
    sort_order_var.set("Ascending")

    refresh_student_table()

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
# Store the current action for the student records page.
record_action = "view"

# Display the main menu heading.
main_heading = Label(
    main,
    text = "MAIN MENU",
    font = ("Times New Roman", 16, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
main_heading.place(x = 20, y = 155, width = 280)

# Display the extensions heading.
extension_heading = Label(
    main,
    text = "EXTENSIONS",
    font = ("Times New Roman", 16, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
extension_heading.place(x = 350, y = 155, width = 280)

# Create the vertical separator.
separator = Frame(
    main,
    bg = "#BDBDBD",
    width = 2,
    height = 330
)
separator.place(x = 325, y = 150)

# MAIN MENU BUTTONS

# Button 1: View All Student Records.
btn_all = Button(
    main,
    text = "All Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("view")
)
btn_all.place(x = 27, y = 200, width = 265, height = 55)

# Button 2: View an individual student record.
btn_individual = Button(
    main,
    text = "Individual Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: individual_frame.place(x = 0, y = 0)
)
btn_individual.place(x = 27, y = 265, width = 265, height = 55)

# Button 3: Show the highest overall mark.
btn_highest = Button(
    main,
    text = "Highest Overall Mark",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: highest_frame.place(x = 0, y = 0)
)
btn_highest.place(x = 27, y = 330, width = 265, height = 55)

# Button 4: Show the lowest overall mark.
btn_lowest = Button(
    main,
    text = "Lowest Overall Mark",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: lowest_frame.place(x = 0, y = 0)
)
btn_lowest.place(x = 27, y = 395, width = 265, height = 55)

# EXTENSION BUTTONS

# Button 5: Sort student records.
btn_sort = Button(
    main,
    text = "Sort Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("sort")
)
btn_sort.place(x = 357, y = 200, width = 265, height = 55)

# Button 6: Add a student record.
btn_add = Button(
    main,
    text = "Add Student Record",
    font = ("Times New Roman", 13, "bold"),
)
btn_add.place(x = 357, y = 265, width = 265, height = 55)

# Button 7: Delete a student record.
btn_delete = Button(
    main,
    text = "Delete Student Record",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("delete")
)
btn_delete.place(x = 357, y = 330, width = 265, height = 55)

# Button 8: Update a student record.
btn_update = Button(
    main,
    text = "Update Student Record",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("update")
)
btn_update.place(x = 357, y = 395, width = 265, height = 55)

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

# Create the sorting controls.
sort_frame = Frame(
    all_students_frame,
    bg = "#FFF1DB"
)
sort_frame.place(x = 25, y = 95, width = 600, height = 45)

# Store the selected sorting category.
sort_by_var = StringVar()
sort_by_var.set("Name")

# Store the selected sorting order.
sort_order_var = StringVar()
sort_order_var.set("Ascending")

# Display the category label.
sort_label = Label(
    sort_frame,
    text = "Sort by:",
    font = ("Times New Roman", 11, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
sort_label.place(x = 0, y = 8)

# Create the category dropdown.
sort_menu = OptionMenu(
    sort_frame,
    sort_by_var,
    "Name",
    "Student Number",
    "Coursework Total",
    "Exam Mark",
    "Overall Percentage",
    "Grade"
)
sort_menu.config(font = ("Times New Roman", 10))
sort_menu.place(x = 65, y = 3, width = 170, height = 35)

# Display the order label.
order_label = Label(
    sort_frame,
    text = "Order:",
    font = ("Times New Roman", 11, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
order_label.place(x = 250, y = 8)

# Create the order dropdown.
order_menu = OptionMenu(
    sort_frame,
    sort_order_var,
    "Ascending",
    "Descending"
)
order_menu.config(font = ("Times New Roman", 10))
order_menu.place(x = 305, y = 3, width = 130, height = 35)

# Create the Apply button.
apply_button = Button(
    sort_frame,
    text = "Apply",
    font = ("Times New Roman", 10, "bold"),
    command = apply_sort
)
apply_button.place(x = 445, y = 3, width = 75, height = 33)

# Create the Reset button.
reset_button = Button(
    sort_frame,
    text = "Reset",
    font = ("Times New Roman", 10, "bold"),
    command = reset_sort
)
reset_button.place(x = 530, y = 3, width = 70, height = 33)

# Create the body area for the student table.
body_frame = Frame(
    all_students_frame,
    bg = "#FFFFFF"
)
body_frame.place(x = 25, y = 135, width = 600, height = 290)

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

# Create the class summary label.
summary_label = Label(
    all_students_frame,
    text = "",
    font = ("Times New Roman", 13, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
summary_label.place(x = 25, y = 95)

# Refreshes the student table with the latest records.
def refresh_student_table(students = None):

    # Remove the previous table contents.
    for widget in body_frame.winfo_children():
        widget.destroy()

    # Load the latest student records.
    if students is None:
        students = load_students()

    total_percentage = 0

    for column, heading_text in enumerate(headings):

        label = Label(
            body_frame,
            text = heading_text,
            font = ("Times New Roman", 11, "bold"),
            bg = "#23314F",
            fg = "white"
        )
        label.grid(row = 0, column = column, sticky = "nsew", padx = 5, pady = 5)

    # Display each student's information.
    for row, student in enumerate(students, start = 1):

        coursework_total, percentage, grade = calculate_results(student)
        total_percentage += percentage

        details = [
            student["name"],
            student["studentNumber"],
            f"{coursework_total} / 60",
            f"{student['examMark']} / 100",
            f"{percentage:.2f}%",
            grade
        ]

        for column, detail in enumerate(details):

            label = Label(
                body_frame,
                text = detail,
                font = ("Times New Roman", 10),
                bg = "white"
            )
            label.grid(row = row, column = column, sticky = "nsew", padx = 2, pady = 2)

    # Calculate the class average.
    number_of_students = len(students)

    if number_of_students > 0:
        average_percentage = total_percentage / number_of_students
    else:
        average_percentage = 0

    # Display the class summary only when viewing all records.
    if record_action == "view":

        summary_label.config(
            text = f"Number of students: {number_of_students}     Average percentage: {average_percentage:.2f}%"
        )
        summary_label.place(x = 25, y = 95)

    else:
        summary_label.place_forget()


# Display the student records when the application starts.
refresh_student_table()

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
    command = back_to_individual_menu
)
back_button.place(x = 250, y = 430, width = 150, height = 35)

## Create the highest overall mark frame.
highest_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the frame title.
heading = Label(
    highest_frame,
    text = "HIGHEST OVERALL MARK",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)


# Retrieve the highest-scoring student's information.
highest_student = show_highest_student()

# Calculate the student's results.
coursework_total, percentage, grade = calculate_results(highest_student)

# Store the information to display.
details = [
    ["Name", highest_student["name"]],
    ["Number", highest_student["studentNumber"]],
    ["Coursework", f"{coursework_total} / 60"],
    ["Exam", f"{highest_student['examMark']} / 100"],
    ["Percentage", f"{percentage:.2f}%"],
    ["Grade", grade]
]

# Load the award badge image.
badge_image = Image.open(rankimage_path)
badge_image = badge_image.resize((60, 60))
badge_photo = ImageTk.PhotoImage(badge_image)

# Display the award badge.
badge_label = Label(
    highest_frame,
    image = badge_photo,
    bg = "#FFF1DB"
)
badge_label.image = badge_photo
badge_label.place(x = 290, y = 360)

# Create the results display area.
result_frame = Frame(
    highest_frame,
    bg = "#FFF1DB"
)
result_frame.place(x = 100, y = 100, width = 450, height = 250)

# Set two columns.
result_frame.grid_columnconfigure(0, weight = 1)
result_frame.grid_columnconfigure(1, weight = 2)

# Display each piece of student information.
for row, detail in enumerate(details):

    # Display the information heading.
    heading_label = Label(
        result_frame,
        text = detail[0] + ":",
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "#FFFFFF",
        width = 10,
        anchor = "w",
        padx = 5
    )
    heading_label.grid(row = row, column = 0, sticky = "nsew", padx = 10, pady = 5, ipady = 4)

    # Display the corresponding value.
    value_label = Label(
        result_frame,
        text = detail[1],
        font = ("Times New Roman", 11),
        bg = "#FFFFFF",
        fg = "#23314F",
        relief = "solid",
        bd = 1
    )
    value_label.grid(row = row, column = 1, sticky = "nsew", padx = 5, pady = 5)


# Create the back button.
back_button = Button(
    highest_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = highest_frame.place_forget
)
back_button.place(x = 250, y = 430, width = 150, height = 35)

## Create the lowest overall mark frame.
lowest_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the frame title.
heading = Label(
    lowest_frame,
    text = "LOWEST OVERALL MARK",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)

# Retrieve the lowest-scoring student's information.
lowest_student = show_lowest_student()

# Calculate the student's results.
coursework_total, percentage, grade = calculate_results(lowest_student)

# Store the information to display.
details = [
    ["Name", lowest_student["name"]],
    ["Number", lowest_student["studentNumber"]],
    ["Coursework", f"{coursework_total} / 60"],
    ["Exam", f"{lowest_student['examMark']} / 100"],
    ["Percentage", f"{percentage:.2f}%"],
    ["Grade", grade]
]

# Create the results display area.
result_frame = Frame(
    lowest_frame,
    bg = "#FFF1DB"
)
result_frame.place(x = 100, y = 130, width = 450, height = 250)

# Set two columns.
result_frame.grid_columnconfigure(0, weight = 1)
result_frame.grid_columnconfigure(1, weight = 2)

# Display each piece of student information.
for row, detail in enumerate(details):

    # Display the information heading.
    heading_label = Label(
        result_frame,
        text = detail[0] + ":",
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "#FFFFFF",
        width = 10,
        anchor = "w",
        padx = 5
    )
    heading_label.grid(row = row, column = 0, sticky = "nsew", padx = 10, pady = 5, ipady = 4)

    # Display the corresponding value.
    value_label = Label(
        result_frame,
        text = detail[1],
        font = ("Times New Roman", 11),
        bg = "#FFFFFF",
        fg = "#23314F",
        relief = "solid",
        bd = 1
    )
    value_label.grid(row = row, column = 1, sticky = "nsew", padx = 5, pady = 5)

# Create the back button.
back_button = Button(
    lowest_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = lowest_frame.place_forget
)
back_button.place(x = 250, y = 430, width = 150, height = 35)



main.mainloop()