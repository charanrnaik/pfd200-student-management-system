"""
PFD200 Mini Project: Student Management System
A small command-line application using Python and SQLite.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("students.db")


class StudentManager:
    """Manage student records stored in a local SQLite database."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    course TEXT NOT NULL,
                    year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 6)
                )
                """
            )

    @staticmethod
    def _validate(name, email, course, year):
        name = name.strip()
        email = email.strip().lower()
        course = course.strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Enter a valid email address.")
        if not course:
            raise ValueError("Course cannot be empty.")
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise ValueError("Year must be a number.")
        if not 1 <= year <= 6:
            raise ValueError("Year must be between 1 and 6.")
        return name, email, course, year

    def add_student(self, name, email, course, year):
        name, email, course, year = self._validate(name, email, course, year)
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    "INSERT INTO students(name,email,course,year) VALUES(?,?,?,?)",
                    (name, email, course, year),
                )
                return cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("A student with that email already exists.") from exc

    def list_students(self):
        with self._connect() as conn:
            return conn.execute(
                "SELECT student_id,name,email,course,year FROM students ORDER BY student_id"
            ).fetchall()

    def search_students(self, keyword):
        keyword = keyword.strip()
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT student_id,name,email,course,year
                FROM students
                WHERE name LIKE ? OR email LIKE ? OR course LIKE ?
                ORDER BY student_id
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
            ).fetchall()

    def update_student(self, student_id, name, email, course, year):
        name, email, course, year = self._validate(name, email, course, year)
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE students
                SET name=?, email=?, course=?, year=?
                WHERE student_id=?
                """,
                (name, email, course, year, int(student_id)),
            )
            if cur.rowcount == 0:
                raise ValueError("Student ID not found.")
        return True

    def delete_student(self, student_id):
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM students WHERE student_id=?", (int(student_id),)
            )
            if cur.rowcount == 0:
                raise ValueError("Student ID not found.")
        return True


def print_students(rows):
    if not rows:
        print("No student records found.")
        return
    print("\nID | Name | Email | Course | Year")
    print("-" * 72)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")


def run():
    manager = StudentManager()
    while True:
        print("\n=== Student Management System ===")
        print("1. Add student")
        print("2. List students")
        print("3. Search students")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                sid = manager.add_student(
                    input("Name: "),
                    input("Email: "),
                    input("Course: "),
                    input("Year: "),
                )
                print(f"Student added successfully. ID: {sid}")
            elif choice == "2":
                print_students(manager.list_students())
            elif choice == "3":
                print_students(manager.search_students(input("Search keyword: ")))
            elif choice == "4":
                sid = input("Student ID: ")
                manager.update_student(
                    sid,
                    input("New name: "),
                    input("New email: "),
                    input("New course: "),
                    input("New year: "),
                )
                print("Student updated successfully.")
            elif choice == "5":
                manager.delete_student(input("Student ID: "))
                print("Student deleted successfully.")
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Invalid menu option.")
        except ValueError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    run()
