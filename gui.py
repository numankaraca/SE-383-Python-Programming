import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from services import StudentManager
from models import Student

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Tracking System")
        self.root.geometry("1000x600")
        
        self.manager = StudentManager()
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Layout
        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # Toolbar
        toolbar = ttk.Frame(self.root, padding=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Button(toolbar, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Student", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Student", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(toolbar, text="View Details / Grades", command=self.view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Manage Attendance", command=self.manage_attendance).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        ttk.Button(toolbar, text="Backup Data", command=self.backup_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.refresh_list).pack(side=tk.RIGHT, padx=5)

        # Search Bar
        search_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        search_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.refresh_list())
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Treeview (Table)
        self.tree_frame = ttk.Frame(self.root, padding=10)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        columns = ("id", "name", "surname", "class", "absence", "average")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("surname", text="Surname")
        self.tree.heading("class", text="Class")
        self.tree.heading("absence", text="Absence")
        self.tree.heading("average", text="Average")
        
        self.tree.column("id", width=0, stretch=tk.NO) # Hidden ID column
        self.tree.column("name", width=150)
        self.tree.column("surname", width=150)
        self.tree.column("class", width=80)
        self.tree.column("absence", width=80, anchor=tk.CENTER)
        self.tree.column("average", width=80, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double click event
        self.tree.bind("<Double-1>", lambda event: self.view_details())

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_term = self.search_var.get().lower()
        students = self.manager.list_students()
        
        for s in students:
            if search_term and (search_term not in s.name.lower() and 
                                search_term not in s.surname.lower()):
                continue
                
            avg = self.manager.calculate_average(s.id)
            self.tree.insert("", tk.END, values=(s.id, s.name, s.surname, s.class_name, s.absence_count, f"{avg:.2f}"))

    def get_selected_id(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student.")
            return None
        return self.tree.item(selected_item[0])['values'][0]

    def add_student(self):
        MainWindow = tk.Toplevel(self.root)
        MainWindow.title("Add Student")
        MainWindow.geometry("300x300")
        
        ttk.Label(MainWindow, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(MainWindow)
        name_entry.pack(pady=5)
        
        ttk.Label(MainWindow, text="Surname:").pack(pady=5)
        surname_entry = ttk.Entry(MainWindow)
        surname_entry.pack(pady=5)
        
        ttk.Label(MainWindow, text="Class:").pack(pady=5)
        class_entry = ttk.Entry(MainWindow)
        class_entry.pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            surname = surname_entry.get().strip()
            cls = class_entry.get().strip()
            
            if name and surname and cls:
                self.manager.add_student(name, surname, cls)
                self.refresh_list()
                MainWindow.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")
                
        ttk.Button(MainWindow, text="Save", command=save).pack(pady=10)

    def edit_student(self):
        s_id = self.get_selected_id()
        if not s_id: return
        
        student = self.manager.get_student(s_id)
        if not student: return
        
        MainWindow = tk.Toplevel(self.root)
        MainWindow.title("Edit Student")
        MainWindow.geometry("300x300")
        
        ttk.Label(MainWindow, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(MainWindow)
        name_entry.insert(0, student.name)
        name_entry.pack(pady=5)
        
        ttk.Label(MainWindow, text="Surname:").pack(pady=5)
        surname_entry = ttk.Entry(MainWindow)
        surname_entry.insert(0, student.surname)
        surname_entry.pack(pady=5)
        
        ttk.Label(MainWindow, text="Class:").pack(pady=5)
        class_entry = ttk.Entry(MainWindow)
        class_entry.insert(0, student.class_name)
        class_entry.pack(pady=5)
        
        def save():
            self.manager.update_student(s_id, name_entry.get(), surname_entry.get(), class_entry.get())
            self.refresh_list()
            MainWindow.destroy()
            
        ttk.Button(MainWindow, text="Update", command=save).pack(pady=10)

    def delete_student(self):
        s_id = self.get_selected_id()
        if not s_id: return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            self.manager.delete_student(s_id)
            self.refresh_list()

    def view_details(self):
        s_id = self.get_selected_id()
        if not s_id: return
        
        student = self.manager.get_student(s_id)
        
        DetailWindow = tk.Toplevel(self.root)
        DetailWindow.title(f"Details: {student.name} {student.surname}")
        DetailWindow.geometry("400x400")
        
        info_frame = ttk.LabelFrame(DetailWindow, text="Student Info", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text=f"Class: {student.class_name}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Absence: {student.absence_count}").pack(anchor=tk.W)
        
        grades_frame = ttk.LabelFrame(DetailWindow, text="Grades", padding=10)
        grades_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        text_area = tk.Text(grades_frame, height=10, width=40)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        def refresh_text():
            text_area.delete('1.0', tk.END)
            for lesson, grades in student.grades.items():
                text_area.insert(tk.END, f"{lesson}: {', '.join(map(str, grades))}\n")
        
        refresh_text()
        
        # Add Grade Section
        add_frame = ttk.Frame(DetailWindow, padding=5)
        add_frame.pack(fill=tk.X)
        
        ttk.Label(add_frame, text="Lesson:").pack(side=tk.LEFT)
        lesson_entry = ttk.Entry(add_frame, width=10)
        lesson_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_frame, text="Grade:").pack(side=tk.LEFT)
        grade_entry = ttk.Entry(add_frame, width=5)
        grade_entry.pack(side=tk.LEFT, padx=5)
        
        def add_grade():
            try:
                lesson = lesson_entry.get().strip()
                grade = int(grade_entry.get().strip())
                self.manager.add_grade(s_id, lesson, grade)
                refresh_text()
                lesson_entry.delete(0, tk.END)
                grade_entry.delete(0, tk.END)
                self.refresh_list() # To update average in main window
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")
        
        ttk.Button(add_frame, text="Add", command=add_grade).pack(side=tk.LEFT, padx=5)

    def manage_attendance(self):
        s_id = self.get_selected_id()
        if not s_id: return
        
        student = self.manager.get_student(s_id)
        
        amount = simpledialog.askinteger("Attendance", 
                                       f"Current Absence: {student.absence_count}\n\nEnter change (e.g. 1 or -1):",
                                       parent=self.root)
        if amount is not None:
            if not self.manager.update_attendance(s_id, amount):
                messagebox.showerror("Error", "Result cannot be negative.")
            self.refresh_list()

    def backup_data(self):
        res = self.manager.backup_data()
        messagebox.showinfo("Backup", res)

    def export_csv(self):
        res = self.manager.export_csv()
        messagebox.showinfo("Export", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
