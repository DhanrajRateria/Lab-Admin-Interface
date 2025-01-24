# Lab Admin Interface

A Python-based application designed to streamline the management of a computer lab. This interface allows admins to manage problem sets, assign problems to students, and track their progress, while providing students with an intuitive interface to interact with their assignments.

## Features

### Admin Interface
- Add, view, and clear problem sets.
- View and clear student data.
- Manage problem assignments efficiently.

### Student Interface
- Log in using a unique identifier.
- View assigned problems and optionally change them (one-time only).
- Select programming languages (C, C++, Java, Python) and open relevant compilers.

### Backend
- SQLite database for persistent storage of problems and student data.
- Random problem assignment and one-time problem change logic.
- Real-time data refresh for a seamless experience.

## Technology Stack
- **Frontend:** Tkinter for GUI.
- **Backend:** SQLite for database operations.
- **Programming Language:** Python.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/lab-admin-interface.git
   cd lab-admin-interface
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
    ```bash
    python admin_ui.py
    python student_ui.py
    ```

Usage:

Admin Actions
1. Add Problems: Enter a problem description and click "Add Problem."
2. View Problems: View all problems in a pop-up dialog.
3. Clear Problems: Remove all problems from the database.
4. Manage Student Data: View student data, refresh it, or clear all records.

Student Actions

1. Log In: Enter your unique number and load your assigned problem.
2. View Problem: See your assigned problem description.
Change Problem: Optionally change your assigned problem (one-time only).
3. Select Language: Choose a programming language and open the corresponding compiler.