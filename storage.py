import json
import os
import shutil
from typing import List, Dict
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'students.json')

def load_data() -> List[Dict]:
    """Loads student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading data: {e}")
        return []

def save_data(data: List[Dict]) -> bool:
    """Save student data to the JSON file."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving data: {e}")
        return False

def backup_data() -> str:
    """Creates a backup of the current data file."""
    if not os.path.exists(DATA_FILE):
        return "No data to backup."
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{DATA_FILE}.{timestamp}.bak"
    
    try:
        shutil.copy2(DATA_FILE, backup_file)
        return f"Backup created: {backup_file}"
    except IOError as e:
        return f"Backup failed: {e}"

def export_to_csv(data: List[Dict]) -> str:
    """Exports student data to a CSV file."""
    if not data:
        return "No data to export."
        
    csv_file = os.path.join(os.path.dirname(DATA_FILE), 'students_export.csv')
    
    try:
        with open(csv_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("ID,Name,Surname,Class,Absence,Grades\n")
            
            for student in data:
                grades_str = "; ".join([f"{k}: {v}" for k, v in student.get('grades', {}).items()])
                line = f"{student.get('id')},{student.get('name')},{student.get('surname')},{student.get('class_name')},{student.get('absence_count')},\"{grades_str}\"\n"
                f.write(line)
                
        return f"Data exported to {csv_file}"
    except IOError as e:
        return f"Export failed: {e}"
