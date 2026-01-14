import sys
import os
from services import StudentManager

def print_menu():
    print("\n--- Student Management System ---")
    print("1. Add Student")
    print("2. List Students")
    print("3. View Student Details")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Grade")
    print("7. Calculate Lesson Average")
    print("8. Calculate General Average")
    print("9. Update Attendance")
    print("10. Backup Data / Export CSV")
    print("11. Exit")
    print("---------------------------------")

def get_input(prompt: str, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if not required or value:
            return value
        print("This field is required.")

def main():
    manager = StudentManager()

    # Demo data prompt
    if not manager.students:
        choice = input("No data found. Add demo students? (y/n): ").lower()
        if choice == 'y':
            s1 = manager.add_student("Ali", "Yilmaz", "10A")
            manager.add_grade(s1.id, "Math", 85)
            manager.add_grade(s1.id, "Physics", 90)
            
            s2 = manager.add_student("Ayse", "Demir", "11B")
            manager.add_grade(s2.id, "Math", 95)
            manager.update_attendance(s2.id, 2)
            
            s3 = manager.add_student("Mehmet", "Kaya", "10A")
            manager.add_grade(s3.id, "History", 70)
            print("Demo students added.")

    while True:
        print_menu()
        choice = input("Select an option (1-11): ")

        try:
            if choice == '1':
                name = get_input("Name: ")
                surname = get_input("Surname: ")
                class_name = get_input("Class: ")
                manager.add_student(name, surname, class_name)
                print("Student added successfully.")

            elif choice == '2':
                sort_opt = input("Sort by (1: Default, 2: Average, 3: Absence): ")
                sort_key = None
                if sort_opt == '2': sort_key = 'average'
                elif sort_opt == '3': sort_key = 'absence'
                
                students = manager.list_students(sort_by=sort_key)
                print(f"\n{'ID':<36} | {'Name':<15} | {'Surname':<15} | {'Class':<5} | {'Absence':<7} | {'Avg':<5}")
                print("-" * 100)
                for s in students:
                    avg = manager.calculate_average(s.id)
                    print(f"{s.id:<36} | {s.name:<15} | {s.surname:<15} | {s.class_name:<5} | {s.absence_count:<7} | {avg:.2f}")

            elif choice == '3':
                s_id = get_input("Student ID: ")
                student = manager.get_student(s_id)
                if student:
                    print(f"\n--- {student.name} {student.surname} ({student.class_name}) ---")
                    print(f"Absence: {student.absence_count}")
                    print("Grades:")
                    for lesson, grades in student.grades.items():
                        print(f"  {lesson}: {grades}")
                else:
                    print("Student not found.")

            elif choice == '4':
                s_id = get_input("Student ID: ")
                print("Leave blank to keep current value.")
                name = get_input("New Name: ", required=False)
                surname = get_input("New Surname: ", required=False)
                class_name = get_input("New Class: ", required=False)
                
                if manager.update_student(s_id, name if name else None, 
                                          surname if surname else None, 
                                          class_name if class_name else None):
                    print("Student updated.")
                else:
                    print("Update failed. Check ID.")

            elif choice == '5':
                s_id = get_input("Student ID to delete: ")
                if manager.delete_student(s_id):
                    print("Student deleted.")
                else:
                    print("Student not found.")

            elif choice == '6':
                s_id = get_input("Student ID: ")
                lesson = get_input("Lesson Name: ")
                try:
                    grade = int(get_input("Grade (0-100): "))
                    if manager.add_grade(s_id, lesson, grade):
                        print("Grade added.")
                    else:
                        print("Failed to add grade.")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            elif choice == '7':
                s_id = get_input("Student ID: ")
                lesson = get_input("Lesson Name: ")
                avg = manager.calculate_average(s_id, lesson)
                print(f"Average for {lesson}: {avg:.2f}")

            elif choice == '8':
                s_id = get_input("Student ID: ")
                avg = manager.calculate_average(s_id)
                print(f"General Average: {avg:.2f}")

            elif choice == '9':
                s_id = get_input("Student ID: ")
                try:
                    amount = int(get_input("Absence change (e.g., 1 or -1): "))
                    if manager.update_attendance(s_id, amount):
                        print("Attendance updated.")
                    else:
                        print("Update failed (check ID or if result is negative).")
                except ValueError:
                    print("Invalid number.")

            elif choice == '10':
                sub_choice = input("1. Backup Data\n2. Export CSV\nSelect: ")
                if sub_choice == '1':
                    print(manager.backup_data())
                elif sub_choice == '2':
                    print(manager.export_csv())
                else:
                    print("Invalid selection.")

            elif choice == '11':
                print("Exiting...")
                break

            else:
                print("Invalid option.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
