import tkinter as tk
from tkinter import ttk, messagebox
from backend.database import (
    setup_database,
    update_language,
    can_change_problem,
    get_student_problem_details
)
from backend.problem_manager import assign_random_problem, change_problem
from backend.language_handler import open_compiler

class StudentUI:
    def __init__(self):
        setup_database()
        self.root = tk.Tk()
        self.root.title("Student Interface - Problem Assignment")
        self.root.geometry("800x600")  # Made wider and taller
        self.root.configure(padx=20, pady=20)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student Info Section
        info_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="Unique Number:").pack(anchor=tk.W)
        self.unique_number_entry = ttk.Entry(info_frame, width=30)
        self.unique_number_entry.pack(fill=tk.X, pady=(5, 10))
        ttk.Button(info_frame, text="Load My Information", 
                  command=self.refresh_problem_display).pack(pady=5)
        
        # Current Problem Display
        self.problem_frame = ttk.LabelFrame(main_frame, text="Current Problem", padding="10")
        self.problem_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status Label
        self.status_label = ttk.Label(self.problem_frame, 
                                    text="No problem assigned yet", 
                                    wraplength=700)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Problem Description
        self.problem_text = tk.Text(self.problem_frame, height=8, wrap=tk.WORD)
        self.problem_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.problem_text.config(state=tk.DISABLED)
        
        # Problem Management Section
        problem_frame = ttk.LabelFrame(main_frame, text="Problem Management", padding="10")
        problem_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(problem_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.assign_btn = ttk.Button(button_frame, text="Assign Problem", 
                                   command=self.assign_problem_action)
        self.assign_btn.pack(side=tk.LEFT, padx=5)
        
        self.change_btn = ttk.Button(button_frame, text="Change Problem (One-time only)", 
                                   command=self.change_problem_action)
        self.change_btn.pack(side=tk.LEFT, padx=5)
        
        # Language Selection Section
        lang_frame = ttk.LabelFrame(main_frame, text="Programming Language", padding="10")
        lang_frame.pack(fill=tk.X)
        
        self.language_var = tk.StringVar()
        for lang in ["C", "C++", "Java", "Python"]:
            ttk.Radiobutton(lang_frame, text=lang, variable=self.language_var, 
                          value=lang).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(lang_frame, text="Open Compiler", 
                  command=self.select_language_action).pack(pady=10)

    def refresh_problem_display(self):
        unique_number = self.unique_number_entry.get()
        if not unique_number:
            messagebox.showerror("Error", "Please enter your unique number!")
            return
            
        # Get student's problem details
        problem_id, description, change_count = get_student_problem_details(unique_number)
        
        # Update status label
        status_text = f"Problem ID: {problem_id if problem_id else 'None'}"
        if change_count is not None:
            if change_count == 0:
                status_text += " | You can still change your problem once"
                self.change_btn["state"] = "normal"
            else:
                status_text += " | You have already used your problem change"
                self.change_btn["state"] = "disabled"
        self.status_label.config(text=status_text)
        
        # Update problem description
        self.problem_text.config(state=tk.NORMAL)
        self.problem_text.delete(1.0, tk.END)
        if description:
            self.problem_text.insert(tk.END, description)
        else:
            self.problem_text.insert(tk.END, "No problem currently assigned.")
        self.problem_text.config(state=tk.DISABLED)

    def assign_problem_action(self):
        unique_number = self.unique_number_entry.get()
        if unique_number:
            result = assign_random_problem(unique_number)
            messagebox.showinfo("Assigned Problem", result)
            self.refresh_problem_display()
        else:
            messagebox.showerror("Error", "Unique number cannot be empty!")

    def change_problem_action(self):
        unique_number = self.unique_number_entry.get()
        if not unique_number:
            messagebox.showerror("Error", "Unique number cannot be empty!")
            return
            
        if not can_change_problem(unique_number):
            messagebox.showerror("Error", 
                "You have already used your one-time problem change!")
            self.change_btn["state"] = "disabled"
            return
            
        if messagebox.askyesno("Confirm Change", 
            "Are you sure you want to change your problem?\n\n"
            "This is a one-time option and cannot be undone!"):
            result = change_problem(unique_number)
            messagebox.showinfo("Change Problem", result)
            self.refresh_problem_display()

    def select_language_action(self):
        unique_number = self.unique_number_entry.get()
        language = self.language_var.get()
        if unique_number and language:
            update_language(unique_number, language)
            open_compiler(language)
        else:
            messagebox.showerror("Error", 
                "Please enter your unique number and select a programming language!")

    def run(self):
        self.root.mainloop()