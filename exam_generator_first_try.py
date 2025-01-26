import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from collections import defaultdict
from random import shuffle
import pandas as pd

def determine_location(course):
    if course in ["CIT 412", "EDS 411", "TMC 411"]:
        return "CUCRID"
    elif course == "EIE 412":
        return "lecture theatre 1"
    elif course == "GEC 410":
        return "lecture theatre 1 and 2"
    elif course.startswith("EIE") or course.startswith("CEN"):
        return "EIE Building"
    else:
        return "No location"

def gen_timetable(course_dict):
    timetable_array = [""] * 21  # Placeholder for timetable
    courses = list(course_dict.keys())
    shuffle(courses)

    var_index = 0
    for course in courses:
        timetable_array[var_index] = course
        unit = course_dict[course]
        distance = 2 if unit >= 2 else 1
        var_index += distance
        if var_index >= len(timetable_array):
            break

    # Convert empty strings in timetable_array to "no exam"
    timetable_array = [course if course else "no exam" for course in timetable_array]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] * 3

    week1 = {days[i]: timetable_array[i] for i in range(6)}
    week2 = {days[i]: timetable_array[i] for i in range(6, 12)}
    week3 = {days[i]: timetable_array[i] for i in range(12, 18)}

    df1 = pd.DataFrame(list(week1.items()), columns=["Day", "Course"])
    df2 = pd.DataFrame(list(week2.items()), columns=["Day", "Course"])
    df3 = pd.DataFrame(list(week3.items()), columns=["Day", "Course"])

    df = pd.concat([df1, df2, df3], keys=["Week 1", "Week 2", "Week 3"])
    df["Location"] = df["Course"].apply(determine_location)
    return df

def add_course(course_dict, course_name, course_unit):
    if course_name in course_dict:
        messagebox.showerror("Error", f"Course {course_name} already exists.")
        return

    total_units = sum(course_dict.values()) + course_unit
    if total_units > 31:
        messagebox.showerror("Error", "Total course units exceed the maximum limit of 31.")
        return

    course_dict[course_name] = course_unit
    messagebox.showinfo("Success", f"Course {course_name} added successfully.")

def drop_course(course_dict, course_name):
    if course_name not in course_dict:
        messagebox.showerror("Error", f"Course {course_name} does not exist.")
        return

    del course_dict[course_name]
    messagebox.showinfo("Success", f"Course {course_name} dropped successfully.")

def export_timetable(df):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Timetable saved to {file_path}.")

def create_gui():
    course_dict = {
        "CEN 416": 2,
        "CEN 434": 2,
        "CIT 412": 0,
        "EIE 411": 3,
        "EIE 412": 3,
        "EIE 416": 3,
        "EIE 418": 3,
        "GEC 410": 3,
        "EDS 411": 1,
        "TMC 411": 1,
    }

    def handle_add_course():
        course_name = course_name_entry.get()
        try:
            course_unit = int(course_unit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Course unit must be an integer.")
            return

        add_course(course_dict, course_name, course_unit)

    def handle_drop_course():
        course_name = course_name_entry.get()
        drop_course(course_dict, course_name)

    def handle_generate():
        df = gen_timetable(course_dict)
        export_timetable(df)

    root = tk.Tk()
    root.title("Exam Timetable Generator")

    tk.Label(root, text="Course Name:").grid(row=0, column=0, padx=10, pady=5)
    course_name_entry = tk.Entry(root)
    course_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Course Unit:").grid(row=1, column=0, padx=10, pady=5)
    course_unit_entry = tk.Entry(root)
    course_unit_entry.grid(row=1, column=1, padx=10, pady=5)

    add_button = tk.Button(root, text="Add Course", command=handle_add_course)
    add_button.grid(row=2, column=0, padx=10, pady=10)

    drop_button = tk.Button(root, text="Drop Course", command=handle_drop_course)
    drop_button.grid(row=2, column=1, padx=10, pady=10)

    generate_button = tk.Button(root, text="Generate Timetable", command=handle_generate)
    generate_button.grid(row=3, column=0, columnspan=2, pady=20)

    root.mainloop()

create_gui()
