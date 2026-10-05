# PFD200 Student Management System

A small Python + SQLite command-line application developed as the PFD200 Professional Development mini-project.

## Purpose
The project develops practical skills in Python object-oriented programming, SQLite database handling, input validation, testing and Git/GitHub documentation.

## Features
- Add student records
- List all students
- Search by name, email or course
- Update student records
- Delete student records
- Input validation
- SQLite persistent storage
- Automated unit tests

## Requirements
- Python 3.10+ recommended
- No third-party packages are required

## Run
```bash
python app.py
```

## Test
```bash
python -m unittest -v test_app.py
```

## Files
- `app.py` – main application
- `test_app.py` – automated tests
- `README.md` – project documentation
- `screenshots/` – evidence images

## Security / quality
The application validates user input and uses parameterized SQL queries rather than concatenating user input into SQL statements.
