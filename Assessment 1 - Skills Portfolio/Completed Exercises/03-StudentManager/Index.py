# ---- IMPORT REQUIRED LIBRARIES ---- #
from tkinter import *
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk


# ---- FILE PATHS ---- #

# Set the base directory.
base_path = os.path.dirname(os.path.abspath(__file__))

# Set the paths for the student records and images.
txt_path = os.path.join(base_path, "Assessment 1 - Skills Portfolio", "A1 - Resources", "studentMarks.txt")
json_path = os.path.join(base_path, "studentMarks.json")
image_path = os.path.join(base_path, "LOGO.png")
rankimage_path = os.path.join(base_path, "HighestRank.png")


# ---- STUDENT DATA MANAGEMENT --- #

# Convert the original TXT file into a JSON database.
def convert_to_json():

    students = []

    # Read the student records from the TXT file.
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

    # Save the student records in JSON format.
    with open(json_path, "w") as file:
        json.dump(students, file, indent = 4)


# Convert the TXT file into JSON (run only once).
# convert_to_json()

# Load student records from the JSON database.
def load_students():

    with open(json_path, "r") as file:
        students = json.load(file)

    return students

# Save updated student records to both files.
def save_students(students):

    # Update the original TXT file.
    with open(txt_path, "w") as file:
        file.write(str(len(students)) + "\n")

        for student in students:
            file.write(
                f"{student['studentNumber']},{student['name']},"
                f"{student['coursework1']},{student['coursework2']},"
                f"{student['coursework3']},{student['examMark']}\n"
            )

    # Update the JSON database.
    with open(json_path, "w") as file:
        json.dump(students, file, indent = 4)


# ---- ADD STUDENT RECORD ---- #

# Validate the information entered for a new student.
def validate_student(name, number, cw1, cw2, cw3, exam):

    # Check that the student name is not empty.
    if name == "":
        messagebox.showerror("Invalid Input", "Please enter a student name.")
        return False

    # Check that the student number contains four digits.
    if not number.isdigit() or not 1000 <= int(number) <= 9999:
        messagebox.showerror("Invalid Input", "Student number must be between 1000 and 9999.")
        return False

    # Check that all marks are valid whole numbers.
    try:
        cw1 = int(cw1)
        cw2 = int(cw2)
        cw3 = int(cw3)
        exam = int(exam)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid whole-number marks.")
        return False

    # Check that coursework marks are between 0 and 20.
    if not all(0 <= mark <= 20 for mark in [cw1, cw2, cw3]):
        messagebox.showerror("Invalid Input", "Coursework marks must be between 0 and 20.")
        return False

    # Check that the exam mark is between 0 and 100.
    if not 0 <= exam <= 100:
        messagebox.showerror("Invalid Input", "Exam mark must be between 0 and 100.")
        return False

    return True

# Add a new student record to the database.
def add_student():

    # Retrieve the information entered into the form.
    name = name_entry.get().strip()
    number = number_entry.get().strip()
    cw1 = cw1_entry.get().strip()
    cw2 = cw2_entry.get().strip()
    cw3 = cw3_entry.get().strip()
    exam = exam_entry.get().strip()

    # Validate the entered information.
    if not validate_student(name, number, cw1, cw2, cw3, exam):
        return

    # Load the existing student records.
    students = load_students()

    # Check whether the student number already exists.
    for student in students:
        if student["studentNumber"] == int(number):
            messagebox.showerror("Duplicate Student", "This student number already exists.")
            return

    # Create the new student record.
    new_student = {
        "studentNumber": int(number),
        "name": name,
        "coursework1": int(cw1),
        "coursework2": int(cw2),
        "coursework3": int(cw3),
        "examMark": int(exam)
    }

    # Add the new record to the student list.
    students.append(new_student)

    # Save the updated records to both files.
    save_students(students)

    # Display a confirmation message.
    messagebox.showinfo("Success", "Student record added successfully.")

    # Clear all input fields.
    for entry in entries:
        entry.delete(0, END)


# ---- STUDENT RESULTS AND CALCULATIONS --- #

# Calculate a student's coursework total, percentage and grade.
def calculate_results(student):

    coursework_total = (
        student["coursework1"] +
        student["coursework2"] +
        student["coursework3"]
    )

    total_mark = coursework_total + student["examMark"]

    percentage = (total_mark / 160) * 100

    # Assign a grade according to the overall percentage.
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

# Format an individual student's results for display.
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

# Retrieve an individual student's results using their number.
def view_individual_student(student_number):

    students = load_students()

    # Search for the matching student number.
    for student in students:
        if student["studentNumber"] == student_number:
            return display_student(student)

    return "Student not found."

# Retrieve the student with the highest overall mark.
def show_highest_student():

    students = load_students()

    highest_student = students[0]

    # Compare the overall marks of all students.
    for student in students:
        if (
            calculate_results(student)[0] + student["examMark"] >
            calculate_results(highest_student)[0] + highest_student["examMark"]
        ):
            highest_student = student

    return highest_student

# Retrieve the student with the lowest overall mark.
def show_lowest_student():

    students = load_students()

    lowest_student = students[0]

    # Compare the overall marks of all students.
    for student in students:
        if (
            calculate_results(student)[0] + student["examMark"] <
            calculate_results(lowest_student)[0] + lowest_student["examMark"]
        ):
            lowest_student = student

    return lowest_student


# ---- STUDENT RECORDS AND SORTING ---- #

# Refresh the student records table.
def refresh_student_table(students = None):

    # Remove the previous table contents.
    for widget in body_frame.winfo_children():
        widget.destroy()

    # Load the latest records if no list is supplied.
    if students is None:
        students = load_students()

    # Display the table headings.
    for column, heading_text in enumerate(headings):

        heading_label = Label(
            body_frame,
            text = heading_text,
            font = ("Times New Roman", 10, "bold"),
            bg = "#23314F",
            fg = "#FFFFFF"
        )

        heading_label.grid(
            row = 0,
            column = column,
            sticky = "nsew",
            padx = 2,
            pady = 2
        )

    total_percentage = 0

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
                bg = "#FFFFFF"
            )

            label.grid(
                row = row,
                column = column,
                sticky = "nsew",
                padx = 2,
                pady = 2
            )

    # Calculate the class average.
    number_of_students = len(students)

    if number_of_students > 0:
        average_percentage = total_percentage / number_of_students
    else:
        average_percentage = 0

    # Display the class summary when viewing all records.
    if record_action == "view":

        summary_label.config(
            text = f"Number of students: {number_of_students}     Average percentage: {average_percentage:.2f}%"
        )
        summary_label.place(x = 30, y = 100)

    else:
        summary_label.place_forget()

# Delete a student record using their name and/or student number.
def delete_student():

    # Retrieve the search information.
    name = delete_name_entry.get().strip()
    number = delete_number_entry.get().strip()

    # Check that at least one search field has been completed.
    if name == "" and number == "":
        messagebox.showerror(
            "Missing Information",
            "Please enter a student name or number."
        )
        return

    # Check that the student number is valid, if provided.
    if number != "" and not number.isdigit():
        messagebox.showerror(
            "Invalid Input",
            "Student number must contain digits only."
        )
        return

    # Load the existing student records.
    students = load_students()

    # Find records matching the entered information.
    matching_students = []

    for student in students:

        name_matches = (
            name == "" or student["name"].lower() == name.lower()
        )

        number_matches = (
            number == "" or student["studentNumber"] == int(number)
        )

        if name_matches and number_matches:
            matching_students.append(student)

    # Check whether a matching student was found.
    if len(matching_students) == 0:
        messagebox.showerror(
            "Student Not Found",
            "No matching student record was found."
        )
        return

    # Avoid deleting the wrong student if names are duplicated.
    if len(matching_students) > 1:
        messagebox.showerror(
            "Multiple Matches",
            "Multiple students have this name. Please enter their student number."
        )
        return

    student = matching_students[0]

    # Ask for confirmation before deleting the record.
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete {student['name']} "
        f"({student['studentNumber']})?"
    )

    if not confirm:
        return

    # Remove the student record.
    students.remove(student)

    # Save the updated records to both files.
    save_students(students)

    # Refresh the displayed student table.
    refresh_student_table()

    # Clear the search fields.
    delete_name_entry.delete(0, END)
    delete_number_entry.delete(0, END)

    messagebox.showinfo(
        "Success",
        "Student record deleted successfully."
    )

# Sort student records according to the selected category and order.
def apply_sort():

    students = load_students()

    # Sort alphabetically by student name.
    if sort_by_var.get() == "Name":
        students.sort(key = lambda student: student["name"].lower())

    # Sort numerically by student number.
    elif sort_by_var.get() == "Student Number":
        students.sort(key = lambda student: student["studentNumber"])

    # Sort according to coursework total.
    elif sort_by_var.get() == "Coursework Total":
        students.sort(key = lambda student: calculate_results(student)[0])

    # Sort according to exam mark.
    elif sort_by_var.get() == "Exam Mark":
        students.sort(key = lambda student: student["examMark"])

    # Sort according to overall percentage.
    elif sort_by_var.get() == "Overall Percentage":
        students.sort(key = lambda student: calculate_results(student)[1])

    # Sort alphabetically by grade.
    elif sort_by_var.get() == "Grade":
        students.sort(key = lambda student: calculate_results(student)[2])

    # Reverse the records if descending order is selected.
    if sort_order_var.get() == "Descending":
        students.reverse()

    # Refresh the table using the sorted records.
    refresh_student_table(students)

# Reset the sorting options and restore the original record order.
def reset_sort():

    sort_by_var.set("Name")
    sort_order_var.set("Ascending")

    refresh_student_table()


# ---- HIGHEST AND LOWEST STUDENT PAGES ---- #

# Refresh the highest overall mark page.
def refresh_highest():

    highest_student = show_highest_student()

    coursework_total, percentage, grade = calculate_results(highest_student)

    details = [
        highest_student["name"],
        highest_student["studentNumber"],
        f"{coursework_total} / 60",
        f"{highest_student['examMark']} / 100",
        f"{percentage:.2f}%",
        grade
    ]

    # Update the displayed student information.
    for row, detail in enumerate(details):
        highest_value_labels[row].config(text = detail)

# Refresh the lowest overall mark page.
def refresh_lowest():

    lowest_student = show_lowest_student()

    coursework_total, percentage, grade = calculate_results(lowest_student)

    details = [
        lowest_student["name"],
        lowest_student["studentNumber"],
        f"{coursework_total} / 60",
        f"{lowest_student['examMark']} / 100",
        f"{percentage:.2f}%",
        grade
    ]

    # Update the displayed student information.
    for row, detail in enumerate(details):
        lowest_value_labels[row].config(text = detail)


# ---- PAGE NAVIGATION AND SEARCH FUNCTIONS ---- #

# Open the student records page for the selected action.
def open_records(action):

    global record_action

    record_action = action

    # Show the relevant controls for the selected action.
    if record_action == "sort":
        sort_frame.place(x = 25, y = 90, width = 600, height = 45)
        delete_frame.place_forget()

    elif record_action == "delete":
        sort_frame.place_forget()
        delete_frame.place(x = 25, y = 90, width = 600, height = 45)

    else:
        sort_frame.place_forget()
        delete_frame.place_forget()

    # Refresh the records before opening the page.
    refresh_student_table()

    all_students_frame.place(x = 0, y = 0)

# Open the highest overall mark page.
def open_highest():

    refresh_highest()
    highest_frame.place(x = 0, y = 0)

# Open the lowest overall mark page.
def open_lowest():

    refresh_lowest()
    lowest_frame.place(x = 0, y = 0)

# Search for and display an individual student's results.
def search_student():

    student_number = student_number_entry.get()

    # Check whether the entered number is valid.
    if student_number.isdigit():

        result = view_individual_student(int(student_number))

        result_label.config(text = result)

    else:
        result_label.config(text = "Please enter a valid student number.")

    # Clear the input field.
    student_number_entry.delete(0, END)

# Return to the main menu and clear the previous search.
def back_to_individual_menu():

    individual_frame.place_forget()

    result_label.config(text = "")
    student_number_entry.delete(0, END)


# ---- MAIN APPLICATION WINDOW ---- #

main = Tk()

main.title("Student Manager")
main.geometry("650x500")
main.configure(bg = "#FFF1DB")
main.resizable(False, False)


# ---- APPLICATION HEADER ---- 3

# Create the header frame.
header = Frame(
    main,
    bg = "#23314F",
    width = 650,
    height = 130
)
header.place(x = 0, y = 0)

# Load and resize the application logo.
pic1 = Image.open(image_path)
pic2 = pic1.resize((90, 90))

logo = ImageTk.PhotoImage(pic2)

# Display the application logo.
imglabel = Label(
    main,
    image = logo,
    bg = "#FFF1DB"
)
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


# ---- MAIN MENU ---- #

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


# ---- Main Menu Buttons ---- #

# Menu Item 1: View all student records.
btn_all = Button(
    main,
    text = "All Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("view")
)
btn_all.place(x = 27, y = 200, width = 265, height = 55)

# Menu Item 2: View an individual student record.
btn_individual = Button(
    main,
    text = "Individual Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: individual_frame.place(x = 0, y = 0)
)
btn_individual.place(x = 27, y = 265, width = 265, height = 55)

# Menu Item 3: Show the highest overall mark.
btn_highest = Button(
    main,
    text = "Highest Overall Mark",
    font = ("Times New Roman", 13, "bold"),
    command = open_highest
)
btn_highest.place(x = 27, y = 330, width = 265, height = 55)

# Menu Item 4: Show the lowest overall mark.
btn_lowest = Button(
    main,
    text = "Lowest Overall Mark",
    font = ("Times New Roman", 13, "bold"),
    command = open_lowest
)
btn_lowest.place(x = 27, y = 395, width = 265, height = 55)


# ---- Extension Buttons ---- #

# Menu Item 5: Sort student records.
btn_sort = Button(
    main,
    text = "Sort Student Records",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("sort")
)
btn_sort.place(x = 357, y = 200, width = 265, height = 55)

# Menu Item 6: Add a student record.
btn_add = Button(
    main,
    text = "Add Student Record",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: add_frame.place(x = 0, y = 0)
)
btn_add.place(x = 357, y = 265, width = 265, height = 55)

# Menu Item 7: Delete a student record.
btn_delete = Button(
    main,
    text = "Delete Student Record",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("delete")
)
btn_delete.place(x = 357, y = 330, width = 265, height = 55)

# Menu Item 8: Update a student record.
btn_update = Button(
    main,
    text = "Update Student Record",
    font = ("Times New Roman", 13, "bold"),
    command = lambda: open_records("update")
)
btn_update.place(x = 357, y = 395, width = 265, height = 55)


# ---- ALL STUDENT RECORDS PAGE ---- #

all_students_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the page heading.
heading = Label(
    all_students_frame,
    text = "ALL STUDENT RECORDS",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)


# ---- Sorting Controls ---- #

sort_frame = Frame(
    all_students_frame,
    bg = "#FFF1DB"
)

# Create the delete search frame.
delete_frame = Frame(all_students_frame, bg = "#FFF1DB")

# Display the student name label.
name_label = Label(
    delete_frame,
    text = "Name:",
    font = ("Times New Roman", 11, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
name_label.place(x = 0, y = 10)

# Create the student name input field.
delete_name_entry = Entry(
    delete_frame,
    font = ("Times New Roman", 10)
)
delete_name_entry.place(x = 50, y = 5, width = 140, height = 30)

# Display the student number label.
number_label = Label(
    delete_frame,
    text = "Number:",
    font = ("Times New Roman", 11, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
number_label.place(x = 205, y = 10)

# Create the student number input field.
delete_number_entry = Entry(
    delete_frame,
    font = ("Times New Roman", 10)
)
delete_number_entry.place(x = 270, y = 5, width = 120, height = 30)

# Create the Delete button.
delete_button = Button(
    delete_frame,
    text = "Delete Student",
    font = ("Times New Roman", 10, "bold"),
    command = delete_student
)
delete_button.place(x = 420, y = 5, width = 150, height = 30)

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


# ---- Student Table ---- #

# Create the table body area.
body_frame = Frame(
    all_students_frame,
    bg = "#FFFFFF"
)
body_frame.place(x = 25, y = 135, width = 600, height = 290)

# Allow the six table columns to expand evenly.
for column in range(6):
    body_frame.grid_columnconfigure(column, weight = 1)

# Store the student table headings.
headings = ["Name", "Number", "Coursework", "Exam", "Percentage", "Grade"]


# ---- Class Summary ---- #

summary_label = Label(
    all_students_frame,
    text = "",
    font = ("Times New Roman", 13, "bold"),
    bg = "#FFF1DB",
    fg = "#23314F"
)
summary_label.place(x = 25, y = 95)

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


# ---- INDIVIDUAL STUDENT RECORDS PAGE ---- #

individual_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the page heading.
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
    text = "Enter Student Number:",
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

# Create the area for displaying student results.
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


# ---- HIGHEST OVERALL MARK PAGE ---- #

highest_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the page heading.
heading = Label(
    highest_frame,
    text = "HIGHEST OVERALL MARK",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)

# Retrieve the highest-scoring student.
highest_student = show_highest_student()

coursework_total, percentage, grade = calculate_results(highest_student)

# Store the student's information for display.
details = [
    ["Name", highest_student["name"]],
    ["Number", highest_student["studentNumber"]],
    ["Coursework", f"{coursework_total} / 60"],
    ["Exam", f"{highest_student['examMark']} / 100"],
    ["Percentage", f"{percentage:.2f}%"],
    ["Grade", grade]
]


# ---- Award Badge ---- #

# Load and resize the award badge image.
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


# ---- Results Display ---- #

result_frame_highest = Frame(
    highest_frame,
    bg = "#FFF1DB"
)
result_frame_highest.place(x = 100, y = 100, width = 450, height = 250)

# Set the two result columns.
result_frame_highest.grid_columnconfigure(0, weight = 1)
result_frame_highest.grid_columnconfigure(1, weight = 2)

# Store the value labels so they can be refreshed.
highest_value_labels = []

# Display each piece of student information.
for row, detail in enumerate(details):

    # Display the information heading.
    heading_label = Label(
        result_frame_highest,
        text = detail[0] + ":",
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "#FFFFFF",
        width = 10,
        anchor = "w",
        padx = 5
    )

    heading_label.grid(
        row = row,
        column = 0,
        sticky = "nsew",
        padx = 10,
        pady = 5,
        ipady = 4
    )


    # Display the corresponding value.
    value_label = Label(
        result_frame_highest,
        text = detail[1],
        font = ("Times New Roman", 11),
        bg = "#FFFFFF",
        fg = "#23314F",
        relief = "solid",
        bd = 1
    )

    value_label.grid(
        row = row,
        column = 1,
        sticky = "nsew",
        padx = 5,
        pady = 5
    )

    highest_value_labels.append(value_label)

# Create the back button.
back_button = Button(
    highest_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = highest_frame.place_forget
)
back_button.place(x = 250, y = 430, width = 150, height = 35)


# ---- LOWEST OVERALL MARK PAGE ---- #

lowest_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the page heading.
heading = Label(
    lowest_frame,
    text = "LOWEST OVERALL MARK",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)

# Retrieve the lowest-scoring student.
lowest_student = show_lowest_student()

coursework_total, percentage, grade = calculate_results(lowest_student)

# Store the student's information for display.
details = [
    ["Name", lowest_student["name"]],
    ["Number", lowest_student["studentNumber"]],
    ["Coursework", f"{coursework_total} / 60"],
    ["Exam", f"{lowest_student['examMark']} / 100"],
    ["Percentage", f"{percentage:.2f}%"],
    ["Grade", grade]
]


# ---- Results Display ---- #

result_frame_lowest = Frame(
    lowest_frame,
    bg = "#FFF1DB"
)
result_frame_lowest.place(x = 100, y = 130, width = 450, height = 250)

# Set the two result columns.
result_frame_lowest.grid_columnconfigure(0, weight = 1)
result_frame_lowest.grid_columnconfigure(1, weight = 2)

# Store the value labels so they can be refreshed.
lowest_value_labels = []

# Display each piece of student information.
for row, detail in enumerate(details):

    # Display the information heading.
    heading_label = Label(
        result_frame_lowest,
        text = detail[0] + ":",
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "#FFFFFF",
        width = 10,
        anchor = "w",
        padx = 5
    )

    heading_label.grid(
        row = row,
        column = 0,
        sticky = "nsew",
        padx = 10,
        pady = 5,
        ipady = 4
    )

    # Display the corresponding value.
    value_label = Label(
        result_frame_lowest,
        text = detail[1],
        font = ("Times New Roman", 11),
        bg = "#FFFFFF",
        fg = "#23314F",
        relief = "solid",
        bd = 1
    )

    value_label.grid(
        row = row,
        column = 1,
        sticky = "nsew",
        padx = 5,
        pady = 5
    )

    lowest_value_labels.append(value_label)

# Create the back button.
back_button = Button(
    lowest_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = lowest_frame.place_forget
)
back_button.place(x = 250, y = 430, width = 150, height = 35)


# ---- ADD STUDENT RECORD PAGE ---- #

add_frame = Frame(
    main,
    bg = "#FFF1DB",
    width = 650,
    height = 500
)

# Display the page heading.
heading = Label(
    add_frame,
    text = "ADD STUDENT RECORD",
    font = ("Times New Roman", 22, "bold"),
    bg = "#23314F",
    fg = "#FFFFFF"
)
heading.place(x = 25, y = 20, width = 600, height = 60)


# ---- Student Form ---- #

form_frame = Frame(
    add_frame,
    bg = "#FFF1DB"
)
form_frame.place(x = 100, y = 120, width = 450, height = 280)

# Set the two form columns.
form_frame.grid_columnconfigure(0, weight = 1)
form_frame.grid_columnconfigure(1, weight = 2)

# Store the student information fields.
fields = [
    "Name",
    "Number",
    "Coursework 1",
    "Coursework 2",
    "Coursework 3",
    "Exam Mark"
]

# Create the input fields.
name_entry = Entry(form_frame)
number_entry = Entry(form_frame)
cw1_entry = Entry(form_frame)
cw2_entry = Entry(form_frame)
cw3_entry = Entry(form_frame)
exam_entry = Entry(form_frame)

# Store all entry widgets in a list.
entries = [
    name_entry,
    number_entry,
    cw1_entry,
    cw2_entry,
    cw3_entry,
    exam_entry
]

# Create each field label and corresponding input box.
for row, field in enumerate(fields):

    # Display the field label.
    field_label = Label(
        form_frame,
        text = field + ":",
        font = ("Times New Roman", 11, "bold"),
        bg = "#23314F",
        fg = "#FFFFFF",
        width = 10,
        anchor = "w",
        padx = 5
    )

    field_label.grid(
        row = row,
        column = 0,
        sticky = "nsew",
        padx = 10,
        pady = 5,
        ipady = 4
    )

    # Configure and position the input field.
    entries[row].config(
        font = ("Times New Roman", 11),
        bg = "#FFFFFF",
        fg = "#23314F",
        relief = "solid",
        bd = 1
    )

    entries[row].grid(
        row = row,
        column = 1,
        sticky = "nsew",
        padx = 5,
        pady = 5
    )


# ---- Form Buttons ---- #

# Create the Add Student button.
add_button = Button(
    add_frame,
    text = "Add Student",
    font = ("Times New Roman", 12, "bold"),
    command = add_student
)
add_button.place(x = 165, y = 430, width = 150, height = 35)

# Create the back button.
back_button = Button(
    add_frame,
    text = "Back to Menu",
    font = ("Times New Roman", 12, "bold"),
    command = add_frame.place_forget
)
back_button.place(x = 335, y = 430, width = 150, height = 35)

# RUN THE APPLICATION #
main.mainloop()