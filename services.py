from typing import List, Optional, Dict
from models import Student
import storage

class StudentManager:
    def __init__(self):
        self.students: List[Student] = []
        self._load_from_storage()

    def _load_from_storage(self):
        """Load data from storage and convert to Student objects."""
        data = storage.load_data()
        self.students = [Student.from_dict(s) for s in data]

    def _save_to_storage(self):
        """Convert Student objects to dicts and save to storage."""
        data = [s.to_dict() for s in self.students]
        storage.save_data(data)

    def add_student(self, name: str, surname: str, class_name: str) -> Student:
        student = Student(name=name, surname=surname, class_name=class_name)
        self.students.append(student)
        self._save_to_storage()
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def delete_student(self, student_id: str) -> bool:
        student = self.get_student(student_id)
        if student:
            self.students.remove(student)
            self._save_to_storage()
            return True
        return False

    def update_student(self, student_id: str, name: Optional[str] = None, 
                       surname: Optional[str] = None, class_name: Optional[str] = None) -> bool:
        student = self.get_student(student_id)
        if not student:
            return False
        
        if name: student.name = name
        if surname: student.surname = surname
        if class_name: student.class_name = class_name
        
        student.update_timestamp()
        self._save_to_storage()
        return True

    def add_grade(self, student_id: str, lesson: str, grade: int) -> bool:
        student = self.get_student(student_id)
        if not student:
            return False
        
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100")

        if lesson not in student.grades:
            student.grades[lesson] = []
        
        student.grades[lesson].append(grade)
        student.update_timestamp()
        self._save_to_storage()
        return True

    def calculate_average(self, student_id: str, lesson: Optional[str] = None) -> float:
        student = self.get_student(student_id)
        if not student:
            return 0.0
        
        if lesson:
            grades = student.grades.get(lesson, [])
            return sum(grades) / len(grades) if grades else 0.0
        else:
            # General average (average of all grades flattened)
            all_grades = []
            for grades in student.grades.values():
                all_grades.extend(grades)
            return sum(all_grades) / len(all_grades) if all_grades else 0.0

    def update_attendance(self, student_id: str, amount: int) -> bool:
        student = self.get_student(student_id)
        if not student:
            return False
        
        new_absence = student.absence_count + amount
        if new_absence < 0:
            return False # Cannot be negative
        
        student.absence_count = new_absence
        student.update_timestamp()
        self._save_to_storage()
        return True

    def list_students(self, sort_by: str = None) -> List[Student]:
        """
        List students, optionally sorted by 'average' or 'absence'.
        """
        if sort_by == 'average':
            # Calculate average for sorting without modifying actual student record just for sort
            return sorted(self.students, 
                          key=lambda s: self.calculate_average(s.id), 
                          reverse=True)
        elif sort_by == 'absence':
            return sorted(self.students, key=lambda s: s.absence_count, reverse=True)
        
        return self.students

    def backup_data(self) -> str:
        return storage.backup_data()

    def export_csv(self) -> str:
        return storage.export_to_csv([s.to_dict() for s in self.students])
