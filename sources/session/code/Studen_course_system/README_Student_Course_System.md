# 🎓 Student Course System

A simple command-line application built in Python to manage students and courses. The project is structured using object-oriented programming principles and organized into a modular architecture.

---

## 📦 Project Structure

- `main.py` – Entry point of the application.
- `model/student.py` – Defines the `Student` class with attributes and behavior.
- `model/course.py` – Defines the `Course` class with attributes and behavior.
- `core/system_manager.py` – Contains the core logic for managing students and courses.
- `requirments.txt` – Requirements file (currently empty).

---

## 🚀 How to Run

Make sure you have Python 3.10+ installed. Then run:

```bash
python main.py
```

The app will launch a simple command-line interface that allows you to:

- Add students or courses
- View all students or courses
- Enroll students in courses
- Exit the program

---

## 🧠 Features

- Object-Oriented Design (Classes for Student and Course)
- Clean, layered architecture (separation of models and logic)
- Easy to extend in the future (e.g., file/database saving, GUI)

---

## 🧬 Folder Layout

```
Studen_course_system/
│
├── main.py
├── __init__.py
├── requirments.txt
│
├── model/
│   ├── __init__.py
│   ├── student.py
│   └── course.py
│
└── core/
    ├── __init__.py
    └── system_manager.py
```

---

## 📌 Notes

- No external libraries are used at the moment.
- `requirments.txt` is empty for now.
- Data is stored in memory only — not persisted to files or a database.

---

## 👩‍💻 Author

This project was developed as a learning exercise using Python.
