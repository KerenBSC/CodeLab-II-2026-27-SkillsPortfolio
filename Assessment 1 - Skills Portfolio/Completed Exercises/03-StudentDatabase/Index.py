from tkinter import *
import json
import os

# Set the file paths for the TXT and JSON files.
txt_path = os.path.join("Assessment 1 - Skills Portfolio", "A1 - Resources", "studentMarks.txt")
json_path = os.path.join("Assessment 1 - Skills Portfolio", "Completed Exercises", "03-StudentDatabase", "studentMarks.json")

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
            display_student(student)

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

main = Tk()
main.title("Alexa's Joke Corner") # Set the window title.
main.geometry("750x550") # Set the window size.
main.configure(bg = "#FFF1DB") # Set the background colour.
main.resizable(False, False) # Prevent the user from resizing the window.



main.mainloop()