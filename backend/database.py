import sqlite3
from typing import Optional

DATABASE_NAME = "lab_admin.db"

def get_connection():
    """Establish connection to the database."""
    return sqlite3.connect(DATABASE_NAME)

def setup_database():
    """Create necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unique_number TEXT UNIQUE NOT NULL,
        assigned_problem INTEGER,
        selected_language TEXT,
        change_count INTEGER DEFAULT 0,
        FOREIGN KEY (assigned_problem) REFERENCES problems(id)
    )
    """)

    conn.commit()
    conn.close()

def add_problem(description):
    """Add a problem to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO problems (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

def get_all_problems():
    """Retrieve all problems from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problems")
    problems = cursor.fetchall()
    conn.close()
    return problems

def clear_all_problems():
    """Clear all problems from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM problems")
    conn.commit()
    conn.close()

def clear_all_students() -> None:
    """Clear all student data and reset the autoincrement counter."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")
    conn.commit()
    conn.close()

def get_random_problem():
    """Retrieve a random problem from the database."""
    import random
    problems = get_all_problems()
    return random.choice(problems)[0] if problems else None

def assign_problem_to_student(unique_number, problem_id):
    """Assign a problem to a student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO students (unique_number, assigned_problem, change_count)
    VALUES (?, ?, 0)
    """, (unique_number, problem_id))
    cursor.execute("""
    UPDATE students SET assigned_problem = ? WHERE unique_number = ?
    """, (problem_id, unique_number))
    conn.commit()
    conn.close()

def update_language(unique_number, language):
    """Update selected programming language."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE students SET selected_language = ? WHERE unique_number = ?
    """, (language, unique_number))
    conn.commit()
    conn.close()

def get_student_data(unique_number=None):
    """Retrieve student data. If unique_number is None, get all student data."""
    conn = get_connection()
    cursor = conn.cursor()
    if unique_number:
        cursor.execute("""
        SELECT * FROM students WHERE unique_number = ?
        """, (unique_number,))
    else:
        cursor.execute("""
        SELECT * FROM students
        """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_problem_description(problem_id: int) -> Optional[str]:
    """
    Get the description of a specific problem.
    
    Args:
        problem_id (int): The ID of the problem
        
    Returns:
        Optional[str]: Problem description or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM problems WHERE id = ?", (problem_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def can_change_problem(unique_number: str) -> bool:
    """Check if student can change their problem (change_count must be 0)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT change_count FROM students 
    WHERE unique_number = ?
    """, (unique_number,))
    result = cursor.fetchone()
    conn.close()
    
    # If student exists and hasn't used their change
    return result is not None and result[0] == 0

def get_student_problem_details(unique_number: str) -> tuple:
    """Get student's current problem details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.assigned_problem, p.description, s.change_count
    FROM students s
    LEFT JOIN problems p ON s.assigned_problem = p.id
    WHERE s.unique_number = ?
    """, (unique_number,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None, None)