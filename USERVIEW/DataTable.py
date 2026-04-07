from PySide6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QHeaderView, QMessageBox,QMenu
    )

from DATA.Commands import (
    get_all_college, add_college,
    get_all_program, add_program,
    get_all_students, add_students, delete_students
    )

class CollegeTable(QWidget):
    def __init__(self):
        super().__init__()
        self.collegetable_setup()

    def collegetable_setup(self):
        college_Layout = QVBoxLayout()

        self.collegeTable = QTableWidget()
        self.collegeTable.setColumnCount(3)
        self.collegeTable.setHorizontalHeaderLabels(["no.", "College Name", "College Code"])
        self.collegeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_college_data()

        college_Layout.addWidget(self.collegeTable)
        self.setLayout(college_Layout)


class ProgramTable(QWidget):
    def __init__(self):
        super().__init__()
        self.programtable_setup()

    def programtable_setup(self):
        program_Layout = QVBoxLayout()

        self.programTable = QTableWidget()
        self.programTable.setColumnCount(3)
        self.programTable.setHorizontalHeaderLabels(["no.", "Program Name", "College ID"])
        self.programTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_program_data()

        program_Layout.addWidget(self.programTable)
        self.setLayout(program_Layout)

class StudentsTable(QWidget):
    def __init__(self ):
        super().__init__()
        self.studentstable_setup()

    def studentstable_setup(self):
        student_Layout = QVBoxLayout()

        self.studentTable = QTableWidget()
        self.studentTable.setColumnCount(7)
        self.studentTable.setHorizontalHeaderLabels(["no.", "Student ID", "First Name", "Last Name", "Gender", "Year", "Program"])
        self.studentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_student_data()

        student_Layout.addWidget(self.studentTable)
        self.setLayout(student_Layout)

    def load_studentTable(self):
        students = get_all_students()
        self.studentTable.setRowCount(len(students))
        for row_no, student in enumerate(students):
            self.studentTable.setItem(row_no, 0, QTableWidgetItem(str(student["id"])))
            self.studentTable.setItem(row_no, 1, QTableWidgetItem(student["students_id"]))
            self.studentTable.setItem(row_no, 2, QTableWidgetItem(student["first_name"]))
            self.studentTable.setItem(row_no, 3, QTableWidgetItem(student["last_name"]))
            self.studentTable.setItem(row_no, 4, QTableWidgetItem(student["gender"]))
            self.studentTable.setItem(row_no, 5, QTableWidgetItem(str(student["year"])))
            self.studentTable.setItem(row_no, 6, QTableWidgetItem(student["program"]))
        
    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.studentTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        self.actions

    def handle_delete(self):
        row = self.studentTable.currentRow()
        student_no = self.studentTable.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete student with ID {student_no}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            delete_students(student_no)
            self.load_studentTable() 