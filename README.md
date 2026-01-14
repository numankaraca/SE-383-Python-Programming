# 🎓 Student Grades and Attendance Tracking System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> A comprehensive Python-based application designed to manage student records, academic grades, and attendance tracking efficiently.

---

## 📋 Table of Contents

-   [Features](#-features)
-   [Project Structure](#-project-structure)
-   [Installation](#-installation)
-   [Usage](#-usage)
-   [Project Details](#-project-details)
-   [Contributors](#-contributors)

---

## ✨ Features

This system provides both a **Command Line Interface (CLI)** and a **Graphical User Interface (GUI)** for flexibility.

*   **👥 Student Management**:
    *   Add, update, delete, and view student profiles with ease.
*   **📊 Grade Tracking**:
    *   Record grades for specific lessons.
    *   Automatically calculate lesson averages and overall GPA.
*   **📅 Attendance Monitoring**:
    *   Track student absences with a simple increment/decrement system.
*   **📈 Data Analysis**:
    *   Sort students by average grade or absence count.
    *   View detailed student performance reports.
*   **💾 Data Persistence**:
    *   All data is automatically saved to JSON files.
    *   **Backup & Export**: Create timestamped backups and export data to CSV.

---

## 📂 Project Structure

```text
SE-383-Python-Programming/
├── main.py          # 🖥️ CLI Entry Point
├── gui.py           # 🎨 GUI Entry Point
├── services.py      # ⚙️ Business Logic & Operations
├── models.py        # 📦 Data Models (Student Class)
├── storage.py       # 💾 File I/O (JSON Handling)
├── data/            # 📁 Data Storage
│   ├── students.json
│   └── backups/
└── README.md        # 📖 Documentation
```

---

## 🚀 Installation

1.  **Prerequisites**: Ensure you have Python 3.x installed.
2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/omerozerf/SE-383-Python-Programming.git
    cd SE-383-Python-Programming
    ```
    *(Note: Replace the URL with your actual repo URL if different)*

3.  **Dependencies**: No external `pip` packages are required. The project uses standard libraries (including `tkinter` for the GUI).

---

## 🖥️ Usage

### 🎨 Graphical User Interface (GUI)
Launch the visual dashboard:
```bash
python gui.py
```

### ⌨️ Command Line Interface (CLI)
Run the terminal-based tool:
```bash
python main.py
```

---

## 🏫 Project Details

| **Course** | **Instructor** |
| :--- | :--- |
| **SE 383 01** – Python Programming | **Önder TOMBUŞ** |

---

## 👥 Contributors

| Student ID | Name | GitHub Profile |
| :--- | :--- | :--- |
| **20 07 06 040** | Yaren Yıldız | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/yarenyildiz) |
| **21 07 06 017** | Muhammed Numan Karaca | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/numankaraca) |
| **21 07 06 028** | Ömer Faruk Özer | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/omerozerf) |
