from frontend.admin_ui import AdminUI
from frontend.student_ui import StudentUI

def main():
    print("="*50)
    print("Lab Problem Management System")
    print("="*50)
    print("\nSelect Interface:")
    print("1. Admin")
    print("2. Student")
    
    while True:
        choice = input("\nEnter your choice (1-2): ")
        if choice == "1":
            admin = AdminUI()
            admin.run()
            break
        elif choice == "2":
            student = StudentUI()
            student.run()
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")

if __name__ == "__main__":
    main()