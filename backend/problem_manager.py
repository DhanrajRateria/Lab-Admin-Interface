from backend.database import get_random_problem, assign_problem_to_student, get_student_data

def assign_random_problem(unique_number):
    """Assign a random problem to a student."""
    problem_id = get_random_problem()
    if problem_id:
        assign_problem_to_student(unique_number, problem_id)
        return f"Assigned Problem ID: {problem_id}"
    else:
        return "No problems available."

def change_problem(unique_number):
    """Allow the student to change their problem once."""
    student_data = get_student_data(unique_number)
    if student_data and student_data[2] < 1:  # Check if change_count < 1
        return assign_random_problem(unique_number)
    else:
        return "You have already changed your problem once."