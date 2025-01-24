import tkinter as tk
from tkinter import ttk, messagebox
from backend.database import (
    add_problem,
    setup_database,
    get_all_problems,
    clear_all_problems,
    get_student_data,
    clear_all_students
)

class AdminUI:
    def __init__(self):
        setup_database()
        self.root = tk.Tk()
        self.root.title("Admin Interface - Problem Management")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Problem Management Section
        problem_frame = ttk.LabelFrame(main_frame, text="Problem Management", padding="10")
        problem_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Problem Entry
        ttk.Label(problem_frame, text="Problem Description:").pack(anchor=tk.W)
        self.problem_entry = ttk.Entry(problem_frame, width=70)
        self.problem_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Buttons Frame
        button_frame = ttk.Frame(problem_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Problem", command=self.add_problem_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View All Problems", command=self.view_problems).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Problems", command=self.clear_problems).pack(side=tk.LEFT, padx=5)
        
        # Student Data Section
        student_frame = ttk.LabelFrame(main_frame, text="Student Data", padding="10")
        student_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create Treeview for student data
        self.tree = ttk.Treeview(student_frame, columns=("ID", "Unique #", "Problem ID", "Language", "Changes"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Unique #", text="Unique #")
        self.tree.heading("Problem ID", text="Problem ID")
        self.tree.heading("Language", text="Language")
        self.tree.heading("Changes", text="Changes")
        
        # Configure column widths
        for col in self.tree["columns"]:
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(student_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack Treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        ttk.Button(student_frame, text="Refresh Student Data", command=self.refresh_student_data).pack(pady=10)
        ttk.Button(student_frame, text="Clear All Student Data", command=self.clear_students).pack(side=tk.LEFT, padx=5)
        
        # Initial data load
        self.refresh_student_data()

    def add_problem_action(self):
        problem = self.problem_entry.get()
        if problem:
            add_problem(problem)
            messagebox.showinfo("Success", "Problem added successfully!")
            self.problem_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Problem description cannot be empty!")

    def view_problems(self):
        problems = get_all_problems()
        if problems:
            text = "\n".join([f"ID: {p[0]} - {p[1]}" for p in problems])
            dialog = tk.Toplevel(self.root)
            dialog.title("All Problems")
            dialog.geometry("600x400")
            
            text_widget = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, text)
            text_widget.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("All Problems", "No problems found.")

    def clear_problems(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all problems?"):
            clear_all_problems()
            messagebox.showinfo("Success", "All problems cleared!")

    def clear_students(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all student data?"):
            clear_all_students()
            messagebox.showinfo("Success", "All student data cleared!")
            self.refresh_student_data()

    def refresh_student_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load new data
        students = get_student_data()
        for student in students:
            self.tree.insert("", tk.END, values=student)

    def run(self):
        self.root.mainloop()