# ---- IMPORT REQUIRED LIBRARIES ---- #

from tkinter import *
from tkinter import messagebox, ttk
import json
import os


# ---- FILE PATHS ---- #

base_path = os.path.dirname(os.path.abspath(__file__))

txt_path = os.path.join(base_path, "..", "..", "A1 - Resources", "studentMarks.txt")
json_path = os.path.join(base_path, "studentMarks.json")
image_path = os.path.join(base_path, "image", "LOGO.png")


# ---- COLOURS AND FONTS ---- #

navy = "#23314F"
cream = "#FFF1DB"
white = "#FFFFFF"
light_blue = "#E9EEF6"
grey = "#68738A"

heading_font = ("Times New Roman", 22, "bold")
normal_font = ("Times New Roman", 11)
button_font = ("Times New Roman", 11, "bold")


# ---- STUDENT DATA MANAGEMENT ---- #

# Convert the original TXT records into JSON.
def convert_to_json():

    students = []

    with open(txt_path, "r") as file:
        file.readline()

        for line in file:
            data = line.strip().split(",")

            if len(data) == 6:
                student = {
                    "studentNumber": int(data[0]),
                    "name": data[1],
                    "coursework1": int(data[2]),
                    "coursework2": int(data[3]),
                    "coursework3": int(data[4]),
                    "examMark": int(data[5])
                }

                students.append(student)

    with open(json_path, "w") as file:
        json.dump(students, file, indent = 4)


# Load student records from JSON.
def load_students():

    if not os.path.exists(json_path):
        convert_to_json()

    with open(json_path, "r") as file:
        students = json.load(file)

    return students


# Save changes to both the TXT and JSON files.
def save_students(students):

    with open(txt_path, "w") as file:
        file.write(str(len(students)) + "\n")

        for student in students:
            file.write(
                f"{student['studentNumber']},{student['name']},"
                f"{student['coursework1']},{student['coursework2']},"
                f"{student['coursework3']},{student['examMark']}\n"
            )

    with open(json_path, "w") as file:
        json.dump(students, file, indent = 4)


# ---- STUDENT RESULTS AND CALCULATIONS ---- #

# Calculate coursework, total marks, percentage and grade.
def calculate_results(student):

    coursework_total = (
        student["coursework1"] +
        student["coursework2"] +
        student["coursework3"]
    )

    total_mark = coursework_total + student["examMark"]
    percentage = (total_mark / 160) * 100

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

    return coursework_total, total_mark, percentage, grade


# Check that the information entered is valid.
def validate_student(name, number, cw1, cw2, cw3, exam):

    if name == "" or "," in name:
        messagebox.showerror("Invalid Input", "Please enter a valid student name.")
        return False

    if not number.isdigit() or not 1000 <= int(number) <= 9999:
        messagebox.showerror("Invalid Input", "Student number must be between 1000 and 9999.")
        return False

    try:
        cw1 = int(cw1)
        cw2 = int(cw2)
        cw3 = int(cw3)
        exam = int(exam)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter whole-number marks.")
        return False

    if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
        messagebox.showerror("Invalid Input", "Each coursework mark must be between 0 and 20.")
        return False

    if not 0 <= exam <= 100:
        messagebox.showerror("Invalid Input", "The exam mark must be between 0 and 100.")
        return False

    return True


# Create a dictionary containing the student information.
def student_data(name, number, cw1, cw2, cw3, exam):

    return {
        "studentNumber": int(number),
        "name": name,
        "coursework1": int(cw1),
        "coursework2": int(cw2),
        "coursework3": int(cw3),
        "examMark": int(exam)
    }


# ---- MAIN WINDOW ---- #

main = Tk()
main.title("Student Manager")

# Set the window size and position.
window_width = 1000
window_height = 600

screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

main.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
main.minsize(900, 600)
main.configure(bg = cream)

# Set the application window icon using LOGO.png.
if os.path.exists(image_path):
    try:
        window_icon = PhotoImage(file = image_path)
        main.iconphoto(True, window_icon)
    except:
        window_icon = None


# ---- MAIN DASHBOARD LAYOUT ---- #

# Create the header.
header = Frame(main, bg = navy, height = 100)
header.pack(side = TOP, fill = X)
header.pack_propagate(False)

# Display the logo in the header.
logo_label = Label(
    header,
    text = "SM",
    font = ("Times New Roman", 25, "bold"),
    bg = white,
    fg = navy,
    width = 3,
    height = 1
)
logo_label.place(x = 22, y = 19)

# Load the logo image if available.
if os.path.exists(image_path):
    try:
        logo_image = PhotoImage(file = image_path)
        logo_label.config(image = logo_image, text = "")
        logo_label.image = logo_image
        logo_label.place(x = 18, y = 10, width = 75, height = 75)
    except:
        pass

# Display the application title.
title_label = Label(
    header,
    text = "STUDENT MANAGER",
    font = ("Times New Roman", 30, "bold"),
    bg = navy,
    fg = white
)
title_label.place(x = 115, y = 27)

subtitle_label = Label(
    header,
    text = "STUDENT RECORDS AND RESULTS",
    font = ("Arial", 9, "bold"),
    bg = navy,
    fg = "#D8DFEA"
)
subtitle_label.place(relx = 1.0, x = -25, y = 43, anchor = "e")


# Create the main area below the header.
main_area = Frame(main, bg = cream)
main_area.pack(fill = BOTH, expand = True, padx = 15, pady = 15)

# Create the sidebar.
sidebar = Frame(main_area, bg = navy, width = 205)
sidebar.pack(side = LEFT, fill = Y, padx = (0, 15))
sidebar.pack_propagate(False)

# Create the content area.
content_frame = Frame(main_area, bg = white)
content_frame.pack(side = LEFT, fill = BOTH, expand = True)


# ---- PAGE DISPLAY FUNCTIONS ---- #

# Clear the previous page content.
def clear_content():

    for widget in content_frame.winfo_children():
        widget.destroy()


# Display a page heading and optional description.
def page_heading(title, description = ""):

    Label(
        content_frame,
        text = title,
        font = heading_font,
        bg = white,
        fg = navy
    ).pack(anchor = "w", padx = 25, pady = (22, 2))

    if description != "":
        Label(
            content_frame,
            text = description,
            font = ("Arial", 10),
            bg = white,
            fg = grey
        ).pack(anchor = "w", padx = 27, pady = (0, 15))


# Create a sidebar navigation button.
def sidebar_button(text, command, parent = None, spacing = 3):

    if parent is None:
        parent = sidebar

    button = Button(
        parent,
        text = text,
        font = button_font,
        bg = navy,
        fg = white,
        activebackground = "#405477",
        activeforeground = white,
        relief = "flat",
        anchor = "w",
        padx = 20,
        command = command
    )

    button.pack(fill = X, padx = 8, pady = spacing, ipady = 7)


# Expand or collapse a sidebar dropdown menu.
def toggle_menu(menu_frame, heading_button, heading_text, next_heading = None):

    if menu_frame.winfo_ismapped():
        menu_frame.pack_forget()
        heading_button.config(text = heading_text + "   +")

    else:
        if next_heading is None:
            menu_frame.pack(fill = X)
        else:
            menu_frame.pack(fill = X, before = next_heading)

        heading_button.config(text = heading_text + "   -")


# Display student records in a table.
def display_table(students, show_summary = False, parent = None):

    if parent is None:
        parent = content_frame

    table_area = Frame(parent, bg = white)
    table_area.pack(fill = BOTH, expand = True, padx = 25, pady = 10)

    columns = ("name", "number", "coursework", "exam", "percentage", "grade")

    table = ttk.Treeview(
        table_area,
        columns = columns,
        show = "headings",
        height = 15
    )

    # Set the table headings.
    table.heading("name", text = "Student Name")
    table.heading("number", text = "Student Number")
    table.heading("coursework", text = "Coursework")
    table.heading("exam", text = "Exam")
    table.heading("percentage", text = "Percentage")
    table.heading("grade", text = "Grade")

    # Adjust the column widths.
    table.column("name", width = 150, minwidth = 120, anchor = "w", stretch = True)
    table.column("number", width = 110, minwidth = 95, anchor = "center", stretch = True)
    table.column("coursework", width = 100, minwidth = 85, anchor = "center", stretch = True)
    table.column("exam", width = 75, minwidth = 65, anchor = "center", stretch = True)
    table.column("percentage", width = 95, minwidth = 80, anchor = "center", stretch = True)
    table.column("grade", width = 55, minwidth = 45, anchor = "center", stretch = True)

    # Add a scrollbar to the table.
    scrollbar = ttk.Scrollbar(table_area, orient = VERTICAL, command = table.yview)
    table.configure(yscrollcommand = scrollbar.set)

    table.pack(side = LEFT, fill = BOTH, expand = True)
    scrollbar.pack(side = RIGHT, fill = Y)

    total_percentage = 0

    # Insert each student's results.
    for student in students:

        coursework, total, percentage, grade = calculate_results(student)
        total_percentage += percentage

        table.insert(
            "",
            END,
            values = (
                f" {student['name']} ",
                f" {student['studentNumber']} ",
                f" {coursework} / 60 ",
                f" {student['examMark']} / 100 ",
                f" {percentage:.2f}% ",
                f" {grade} "
            )
        )

    # Display the class summary when requested.
    if show_summary:

        number_of_students = len(students)

        if number_of_students > 0:
            average_percentage = total_percentage / number_of_students
        else:
            average_percentage = 0

        summary = Frame(parent, bg = light_blue)
        summary.pack(fill = X, padx = 25, pady = (0, 20))

        Label(
            summary,
            text = f"TOTAL STUDENTS: {number_of_students}",
            font = ("Arial", 10, "bold"),
            bg = light_blue,
            fg = navy
        ).pack(side = LEFT, padx = 18, pady = 14)

        Label(
            summary,
            text = f"CLASS AVERAGE: {average_percentage:.2f}%",
            font = ("Arial", 10, "bold"),
            bg = light_blue,
            fg = navy
        ).pack(side = LEFT, padx = 18, pady = 14)


# Display all the information for one student.
def display_student_details(student):

    coursework, total, percentage, grade = calculate_results(student)

    details = [
        ("Student Name", student["name"]),
        ("Student Number", student["studentNumber"]),
        ("Coursework Total", f"{coursework} / 60"),
        ("Exam Mark", f"{student['examMark']} / 100"),
        ("Overall Mark", f"{total} / 160"),
        ("Overall Percentage", f"{percentage:.2f}%"),
        ("Grade", grade)
    ]

    details_frame = Frame(content_frame, bg = light_blue)
    details_frame.pack(fill = X, padx = 30, pady = 20)

    for row, detail in enumerate(details):

        # Add extra space around the first and last rows.
        if row == 0:
            row_padding = (22, 10)
        elif row == len(details) - 1:
            row_padding = (10, 22)
        else:
            row_padding = 10

        Label(
            details_frame,
            text = detail[0],
            font = ("Arial", 10, "bold"),
            bg = light_blue,
            fg = navy,
            anchor = "w"
        ).grid(row = row, column = 0, sticky = "w", padx = 20, pady = row_padding)

        Label(
            details_frame,
            text = detail[1],
            font = ("Arial", 10),
            bg = light_blue,
            fg = navy,
            anchor = "w"
        ).grid(row = row, column = 1, sticky = "w", padx = 35, pady = row_padding)


# ---- DASHBOARD HOME ---- #

def show_dashboard():

    clear_content()
    students = load_students()

    page_heading(
        "Welcome to Student Manager",
        "Manage student records and analyse class results."
    )

    total_students = len(students)

    # Calculate the class average and highest and lowest results.
    if total_students > 0:
        percentages = [calculate_results(student)[2] for student in students]
        average = sum(percentages) / total_students

        highest = max(students, key = lambda student: calculate_results(student)[1])
        lowest = min(students, key = lambda student: calculate_results(student)[1])

    else:
        average = 0
        highest = None
        lowest = None

    # Display the dashboard summary cards.
    cards = Frame(content_frame, bg = white)
    cards.pack(fill = X, padx = 25, pady = 25)

    card_details = [
        ("TOTAL STUDENTS", str(total_students)),
        ("CLASS AVERAGE", f"{average:.2f}%"),
        ("HIGHEST GRADE", calculate_results(highest)[3] if highest else "-")
    ]

    for title, value in card_details:

        card = Frame(cards, bg = light_blue, padx = 20, pady = 18)
        card.pack(side = LEFT, fill = BOTH, expand = True, padx = 7)

        Label(
            card,
            text = title,
            font = ("Arial", 9, "bold"),
            bg = light_blue,
            fg = grey
        ).pack(anchor = "w")

        Label(
            card,
            text = value,
            font = ("Arial", 23, "bold"),
            bg = light_blue,
            fg = navy
        ).pack(anchor = "w", pady = (8, 0))

    Label(
        content_frame,
        text = "QUICK OVERVIEW",
        font = ("Arial", 12, "bold"),
        bg = white,
        fg = navy
    ).pack(anchor = "w", padx = 32, pady = (20, 5))

    # Show the students with the highest and lowest marks.
    if highest is not None:

        Label(
            content_frame,
            text = f"Highest overall mark: {highest['name']}  |  {calculate_results(highest)[2]:.2f}%",
            font = normal_font,
            bg = white,
            fg = navy
        ).pack(anchor = "w", padx = 32, pady = 7)

        Label(
            content_frame,
            text = f"Lowest overall mark: {lowest['name']}  |  {calculate_results(lowest)[2]:.2f}%",
            font = normal_font,
            bg = white,
            fg = navy
        ).pack(anchor = "w", padx = 32, pady = 7)

    Label(
        content_frame,
        text = "Choose an option from the sidebar to get started.",
        font = ("Arial", 10, "italic"),
        bg = white,
        fg = grey
    ).pack(anchor = "w", padx = 32, pady = 25)


# ---- 1. VIEW ALL STUDENT RECORDS ---- #

def show_all_records():

    clear_content()
    page_heading("All Student Records", "A complete overview of the class.")
    display_table(load_students(), True)


# ---- 2. VIEW AN INDIVIDUAL STUDENT ---- #

def show_individual():

    clear_content()

    page_heading(
        "Individual Student Record",
        "Search using a student's four-digit number."
    )

    search_area = Frame(content_frame, bg = light_blue)
    search_area.pack(fill = X, padx = 30, pady = 20)

    Label(
        search_area,
        text = "Student Number:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).pack(side = LEFT, padx = (18, 8), pady = 18)

    number_entry = Entry(search_area, font = normal_font, width = 18)
    number_entry.pack(side = LEFT, pady = 18)

    # Find and display the matching student.
    def search():

        number = number_entry.get().strip()

        if not number.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid student number.")
            return

        students = load_students()

        for student in students:
            if student["studentNumber"] == int(number):
                clear_content()
                page_heading("Student Record", "Individual student results.")
                display_student_details(student)
                return

        messagebox.showerror("Not Found", "No student with that number was found.")

    Button(
        search_area,
        text = "Search",
        font = button_font,
        bg = navy,
        fg = white,
        command = search,
        relief = "flat",
        padx = 18
    ).pack(side = LEFT, padx = 12, pady = 15)


# ---- 3. HIGHEST OVERALL MARK ---- #

def show_highest():

    clear_content()
    students = load_students()

    page_heading("Highest Overall Mark", "The student with the highest total score.")

    if len(students) == 0:
        Label(
            content_frame,
            text = "No student records available.",
            bg = white
        ).pack(pady = 30)
        return

    highest = max(students, key = lambda student: calculate_results(student)[1])
    display_student_details(highest)


# ---- 4. LOWEST OVERALL MARK ---- #

def show_lowest():

    clear_content()
    students = load_students()

    page_heading("Lowest Overall Mark", "The student with the lowest total score.")

    if len(students) == 0:
        Label(
            content_frame,
            text = "No student records available.",
            bg = white
        ).pack(pady = 30)
        return

    lowest = min(students, key = lambda student: calculate_results(student)[1])
    display_student_details(lowest)


# ---- 5. SORT STUDENT RECORDS ---- #

def show_sort():

    clear_content()
    page_heading("Sort Student Records", "Choose a category and sorting order.")

    options = Frame(content_frame, bg = light_blue)
    options.pack(fill = X, padx = 30, pady = 20)

    Label(
        options,
        text = "Sort by:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 0, column = 0, padx = 15, pady = 18)

    sort_by = StringVar(value = "Name")

    sort_menu = OptionMenu(
        options,
        sort_by,
        "Name",
        "Student Number",
        "Coursework Total",
        "Exam Mark",
        "Overall Percentage",
        "Grade"
    )
    sort_menu.grid(row = 0, column = 1, padx = 10, pady = 15)

    Label(
        options,
        text = "Order:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 0, column = 2, padx = 15, pady = 18)

    sort_order = StringVar(value = "Ascending")

    order_menu = OptionMenu(
        options,
        sort_order,
        "Ascending",
        "Descending"
    )
    order_menu.grid(row = 0, column = 3, padx = 10, pady = 15)

    # Keep the sorting controls visible when the results refresh.
    results_heading = Label(
        content_frame,
        text = "Student Records",
        font = ("Arial", 11, "bold"),
        bg = white,
        fg = navy
    )
    results_heading.pack(anchor = "w", padx = 27, pady = (5, 0))

    results_frame = Frame(content_frame, bg = white)
    results_frame.pack(fill = BOTH, expand = True)

    # Sort the records using the selected category and order.
    def apply_sort():

        students = load_students()
        category = sort_by.get()

        if category == "Name":
            students.sort(key = lambda student: student["name"].lower())

        elif category == "Student Number":
            students.sort(key = lambda student: student["studentNumber"])

        elif category == "Coursework Total":
            students.sort(key = lambda student: calculate_results(student)[0])

        elif category == "Exam Mark":
            students.sort(key = lambda student: student["examMark"])

        elif category == "Overall Percentage":
            students.sort(key = lambda student: calculate_results(student)[2])

        elif category == "Grade":
            students.sort(key = lambda student: calculate_results(student)[3])

        if sort_order.get() == "Descending":
            students.reverse()

        results_heading.config(
            text = f"Sorted by {category} ({sort_order.get()})"
        )

        for widget in results_frame.winfo_children():
            widget.destroy()

        display_table(students, parent = results_frame)

    Button(
        options,
        text = "Apply Sort",
        font = button_font,
        bg = navy,
        fg = white,
        relief = "flat",
        command = apply_sort,
        padx = 15
    ).grid(row = 0, column = 4, padx = 15, pady = 15)

    display_table(load_students(), parent = results_frame)


# ---- 6. ADD A STUDENT RECORD ---- #

def show_add_student():

    clear_content()

    page_heading("Add Student Record", "Enter the student's information below.")

    form = Frame(content_frame, bg = light_blue)
    form.pack(fill = X, padx = 35, pady = 15)

    fields = [
        "Student Name",
        "Student Number",
        "Coursework 1",
        "Coursework 2",
        "Coursework 3",
        "Exam Mark"
    ]

    entries = []

    # Create an input field for each student detail.
    for row, field in enumerate(fields):

        Label(
            form,
            text = field + ":",
            font = button_font,
            bg = light_blue,
            fg = navy
        ).grid(row = row, column = 0, sticky = "w", padx = 20, pady = 9)

        entry = Entry(form, font = normal_font, width = 30)
        entry.grid(row = row, column = 1, sticky = "w", padx = 20, pady = 9)

        entries.append(entry)

    # Validate and save the new student record.
    def add_student():

        name = entries[0].get().strip()
        number = entries[1].get().strip()
        cw1 = entries[2].get().strip()
        cw2 = entries[3].get().strip()
        cw3 = entries[4].get().strip()
        exam = entries[5].get().strip()

        if not validate_student(name, number, cw1, cw2, cw3, exam):
            return

        students = load_students()

        for student in students:
            if student["studentNumber"] == int(number):
                messagebox.showerror("Duplicate Student", "That student number already exists.")
                return

        students.append(student_data(name, number, cw1, cw2, cw3, exam))
        save_students(students)

        messagebox.showinfo("Success", "Student record added successfully.")
        show_add_student()

    Button(
        content_frame,
        text = "Add Student",
        font = button_font,
        bg = navy,
        fg = white,
        relief = "flat",
        command = add_student,
        padx = 25,
        pady = 8
    ).pack(pady = 12)


# ---- FIND A STUDENT BY NAME OR NUMBER ---- #

# Return students matching the entered name and/or number.
def find_matching_student(name, number):

    students = load_students()
    matches = []

    for student in students:

        name_matches = name == "" or student["name"].lower() == name.lower()
        number_matches = number == "" or student["studentNumber"] == int(number)

        if name_matches and number_matches:
            matches.append(student)

    return matches


# ---- 7. DELETE A STUDENT RECORD ---- #

def show_delete_student():

    clear_content()

    page_heading(
        "Delete Student Record",
        "Find a student using their name or student number."
    )

    form = Frame(content_frame, bg = light_blue)
    form.pack(fill = X, padx = 30, pady = 20)

    Label(
        form,
        text = "Student Name:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 0, column = 0, sticky = "w", padx = 15, pady = 15)

    name_entry = Entry(form, font = normal_font, width = 22)
    name_entry.grid(row = 0, column = 1, padx = 10, pady = 15)

    Label(
        form,
        text = "Student Number:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 1, column = 0, sticky = "w", padx = 15, pady = 15)

    number_entry = Entry(form, font = normal_font, width = 22)
    number_entry.grid(row = 1, column = 1, padx = 10, pady = 15)

    # Find the record and ask for confirmation before deleting it.
    def delete_student():

        name = name_entry.get().strip()
        number = number_entry.get().strip()

        if name == "" and number == "":
            messagebox.showerror("Missing Information", "Enter a name or student number.")
            return

        if number != "" and not number.isdigit():
            messagebox.showerror("Invalid Input", "Student number must contain digits only.")
            return

        matches = find_matching_student(name, number)

        if len(matches) == 0:
            messagebox.showerror("Not Found", "No matching student was found.")
            return

        if len(matches) > 1:
            messagebox.showerror("Multiple Matches", "Enter the student number to identify the correct student.")
            return

        students = load_students()
        student = matches[0]

        if len(students) == 1:
            messagebox.showerror("Cannot Delete", "At least one student record must remain.")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {student['name']} ({student['studentNumber']})?"
        )

        if confirm:
            students.remove(student)
            save_students(students)

            messagebox.showinfo("Success", "Student record deleted successfully.")
            show_delete_student()

    Button(
        form,
        text = "Delete Student",
        font = button_font,
        bg = navy,
        fg = white,
        relief = "flat",
        command = delete_student,
        padx = 15
    ).grid(row = 2, column = 1, pady = 15)


# ---- 8. UPDATE A STUDENT RECORD ---- #

def show_update_student():

    clear_content()

    page_heading(
        "Update Student Record",
        "Search for a student, then edit their information."
    )

    search_form = Frame(content_frame, bg = light_blue)
    search_form.pack(fill = X, padx = 30, pady = 15)

    Label(
        search_form,
        text = "Student Name:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 0, column = 0, sticky = "w", padx = 15, pady = 12)

    name_entry = Entry(search_form, font = normal_font, width = 22)
    name_entry.grid(row = 0, column = 1, padx = 10, pady = 12)

    Label(
        search_form,
        text = "Student Number:",
        font = button_font,
        bg = light_blue,
        fg = navy
    ).grid(row = 1, column = 0, sticky = "w", padx = 15, pady = 12)

    number_entry = Entry(search_form, font = normal_font, width = 22)
    number_entry.grid(row = 1, column = 1, padx = 10, pady = 12)

    # Find the student whose details need to be changed.
    def find_student():

        name = name_entry.get().strip()
        number = number_entry.get().strip()

        if name == "" and number == "":
            messagebox.showerror("Missing Information", "Enter a name or student number.")
            return

        if number != "" and not number.isdigit():
            messagebox.showerror("Invalid Input", "Student number must contain digits only.")
            return

        matches = find_matching_student(name, number)

        if len(matches) == 0:
            messagebox.showerror("Not Found", "No matching student was found.")
            return

        if len(matches) > 1:
            messagebox.showerror("Multiple Matches", "Enter the student number to identify the correct student.")
            return

        student = matches[0]
        show_edit_form(student)

    Button(
        search_form,
        text = "Find Student",
        font = button_font,
        bg = navy,
        fg = white,
        relief = "flat",
        command = find_student,
        padx = 15
    ).grid(row = 2, column = 1, pady = 12)


# Display the selected student's details in editable fields.
def show_edit_form(student):

    clear_content()

    page_heading(
        "Edit Student Details",
        f"Editing the record for {student['name']}."
    )

    form = Frame(content_frame, bg = light_blue)
    form.pack(fill = X, padx = 35, pady = 15)

    fields = [
        ("Student Name", student["name"]),
        ("Student Number", str(student["studentNumber"])),
        ("Coursework 1", str(student["coursework1"])),
        ("Coursework 2", str(student["coursework2"])),
        ("Coursework 3", str(student["coursework3"])),
        ("Exam Mark", str(student["examMark"]))
    ]

    entries = []

    # Fill each field with the student's existing information.
    for row, field in enumerate(fields):

        Label(
            form,
            text = field[0] + ":",
            font = button_font,
            bg = light_blue,
            fg = navy
        ).grid(row = row, column = 0, sticky = "w", padx = 20, pady = 8)

        entry = Entry(form, font = normal_font, width = 30)
        entry.insert(0, field[1])
        entry.grid(row = row, column = 1, sticky = "w", padx = 20, pady = 8)

        entries.append(entry)

    original_number = student["studentNumber"]

    # Validate and save the updated student details.
    def update_student():

        name = entries[0].get().strip()
        number = entries[1].get().strip()
        cw1 = entries[2].get().strip()
        cw2 = entries[3].get().strip()
        cw3 = entries[4].get().strip()
        exam = entries[5].get().strip()

        if not validate_student(name, number, cw1, cw2, cw3, exam):
            return

        students = load_students()

        # Prevent the updated number from matching another student.
        for current_student in students:
            if current_student["studentNumber"] == int(number) and int(number) != original_number:
                messagebox.showerror("Duplicate Student", "That student number already exists.")
                return

        updated_student = student_data(name, number, cw1, cw2, cw3, exam)

        for index, current_student in enumerate(students):
            if current_student["studentNumber"] == original_number:
                students[index] = updated_student
                break

        save_students(students)

        messagebox.showinfo("Success", "Student record updated successfully.")
        show_update_student()

    Button(
        content_frame,
        text = "Save Changes",
        font = button_font,
        bg = navy,
        fg = white,
        relief = "flat",
        command = update_student,
        padx = 25,
        pady = 8
    ).pack(pady = 12)


# ---- SIDEBAR MENU ---- #

# Dashboard navigation button.
sidebar_button("⌂   Dashboard", show_dashboard, spacing = (25, 3))


# ---- MAIN MENU DROPDOWN ---- #

main_menu_heading = Button(
    sidebar,
    text = "MAIN MENU   +",
    font = ("Arial", 10, "bold"),
    bg = "#405477",
    fg = white,
    activebackground = "#52688D",
    activeforeground = white,
    relief = "flat",
    anchor = "w",
    padx = 18,
    command = lambda: toggle_menu(
        main_menu_frame,
        main_menu_heading,
        "MAIN MENU",
        extensions_heading
    )
)
main_menu_heading.pack(fill = X, padx = 8, pady = (18, 3), ipady = 9)

main_menu_frame = Frame(sidebar, bg = navy)

sidebar_button("1   All Student Records", show_all_records, main_menu_frame)
sidebar_button("2   Individual Record", show_individual, main_menu_frame)
sidebar_button("3   Highest Mark", show_highest, main_menu_frame)
sidebar_button("4   Lowest Mark", show_lowest, main_menu_frame)


# ---- EXTENSIONS DROPDOWN ---- #

extensions_heading = Button(
    sidebar,
    text = "EXTENSIONS   +",
    font = ("Arial", 10, "bold"),
    bg = "#405477",
    fg = white,
    activebackground = "#52688D",
    activeforeground = white,
    relief = "flat",
    anchor = "w",
    padx = 18,
    command = lambda: toggle_menu(
        extensions_frame,
        extensions_heading,
        "EXTENSIONS"
    )
)
extensions_heading.pack(fill = X, padx = 8, pady = (12, 3), ipady = 9)

extensions_frame = Frame(sidebar, bg = navy)

sidebar_button("5   Sort Records", show_sort, extensions_frame)
sidebar_button("6   Add Student", show_add_student, extensions_frame)
sidebar_button("7   Delete Student", show_delete_student, extensions_frame)
sidebar_button("8   Update Student", show_update_student, extensions_frame)


# Keep both dropdown menus collapsed when the app opens.
main_menu_frame.pack_forget()
extensions_frame.pack_forget()


# Sidebar footer.
Label(
    sidebar,
    text = "STUDENT MANAGER",
    font = ("Arial", 8, "bold"),
    bg = navy,
    fg = "#AEBBD0"
).pack(side = BOTTOM, pady = 18)


# ---- TABLE STYLE ---- #

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background = white,
    foreground = navy,
    rowheight = 32,
    fieldbackground = white,
    font = ("Arial", 9)
)

style.configure(
    "Treeview.Heading",
    background = navy,
    foreground = white,
    font = ("Arial", 9, "bold"),
    padding = 8
)

style.map(
    "Treeview",
    background = [("selected", "#D7E1F0")],
    foreground = [("selected", navy)]
)


# ---- RUN THE APPLICATION ---- #

show_dashboard()
main.mainloop()