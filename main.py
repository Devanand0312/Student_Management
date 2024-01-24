import sqlite3
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox

class Student:
    def __init__(self, roll_number, name, age, grade):
        self.roll_number = roll_number
        self.name = name
        self.age = age
        self.grade = grade

class StudentManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll_number TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_student(self, student):
        self.cursor.execute('''
            INSERT INTO students (roll_number, name, age, grade)
            VALUES (?, ?, ?, ?)
        ''', (student.roll_number, student.name, student.age, student.grade))
        self.conn.commit()

    def display_students(self):
        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()
        return students

    def search_student(self, roll_number):
        self.cursor.execute("SELECT * FROM students WHERE roll_number=?", (roll_number,))
        student = self.cursor.fetchone()
        return student

class StudentManagementGUI:
    def __init__(self, master):
        self.master = master
        master.title("Student Management System")

        self.label = Label(master, text="Roll Number:")
        self.label.grid(row=0, column=0)

        self.roll_number_entry = Entry(master)
        self.roll_number_entry.grid(row=0, column=1)

        self.search_button = Button(master, text="Search", command=self.search_student)
        self.search_button.grid(row=0, column=2)

        self.display_button = Button(master, text="Display Students", command=self.display_students)
        self.display_button.grid(row=1, column=0, columnspan=3)

        self.message_label = Label(master, text="")
        self.message_label.grid(row=2, column=0, columnspan=3)

    def search_student(self):
        roll_number = self.roll_number_entry.get()
        if roll_number:
            student = sms.search_student(roll_number)
            if student:
                self.message_label.config(text=f"Student found - Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
            else:
                self.message_label.config(text="Student not found.")
        else:
            self.message_label.config(text="Please enter Roll Number.")

    def display_students(self):
        students = sms.display_students()
        if students:
            for student in students:
                print(f"Roll Number: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
        else:
            print("No students in the system.")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

if __name__ == "__main__":
    sms = StudentManagementSystem()

    root = Tk()
    gui = StudentManagementGUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
