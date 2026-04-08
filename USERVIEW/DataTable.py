from PySide6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QMessageBox,QMenu
    )
from PySide6.QtCore import Qt

from DATA.Commands import (
    get_all_college, add_college, delete_college,
    get_all_program, add_program, delete_program,
    get_all_students, add_students, delete_students
    )
from USERVIEW.AddEdit import (
    EditCollegeDialog, EditProgramDialog, EditStudentDialog
    )


#COLLEGE FUNCTIONS
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
        self.load_collegeTable()

        self.collegeTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.collegeTable.customContextMenuRequested.connect(self.show_contextMenu)

        college_Layout.addWidget(self.collegeTable)
        self.setLayout(college_Layout)

    def load_collegeTable(self):
        college = get_all_college()
        self.collegeTable.setRowCount(len(college))
        for row_no, college in enumerate(college):
            self.collegeTable.setItem(row_no, 0, QTableWidgetItem(str(college["id"])))
            self.collegeTable.setItem(row_no, 1, QTableWidgetItem(college["college_name"]))
            self.collegeTable.setItem(row_no, 2, QTableWidgetItem(college["college_code"]))

    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.collegeTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        row = self.collegeTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a college to edit.")
            return 
        college_id = self.collegeTable.item(row, 0).text()
        dialog = EditCollegeDialog(college_id, self)
        dialog.college_updated.connect(self.load_collegeTable)
        dialog.exec()

    def handle_delete(self):
        row = self.collegeTable.currentRow()
        college_name = self.collegeTable.item(row, 1).text()
        confirm = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to college this college {college_name}?\n\n"
            "Warning: This will also delete all associated Programs and "
            "unassign Students!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            delete_college(college_name)
            self.load_collegeTable() 


# PROGRAM FUNCTIONS
class ProgramTable(QWidget):
    def __init__(self):
        super().__init__()
        self.programtable_setup()

    def programtable_setup(self):
        program_Layout = QVBoxLayout()

        self.programTable = QTableWidget()
        self.programTable.setColumnCount(4)
        self.programTable.setHorizontalHeaderLabels(["no.","Program Code", "Program Name", "College ID"])
        self.programTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_programTable()

        self.programTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.programTable.customContextMenuRequested.connect(self.show_contextMenu)

        program_Layout.addWidget(self.programTable)
        self.setLayout(program_Layout)

    def load_programTable(self):
        program = get_all_program()
        self.programTable.setRowCount(len(program))
        for row_no, program in enumerate(program):
            self.programTable.setItem(row_no, 0, QTableWidgetItem(str(program["id"])))
            self.programTable.setItem(row_no, 1, QTableWidgetItem(program["program_code"]))
            self.programTable.setItem(row_no, 2, QTableWidgetItem(program["program_name"]))
            self.programTable.setItem(row_no, 3, QTableWidgetItem(str(program["college_code"])))

    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.programTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        row = self.programTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a program to edit.")
            return 
        program_id = self.programTable.item(row, 0).text()
        dialog = EditProgramDialog(program_id, self)
        dialog.program_updated.connect(self.load_programTable)
        dialog.exec()

    def handle_delete(self):
        row = self.programTable.currentRow()
        program_name = self.programTable.item(row, 1).text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete this program {program_name}?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            delete_program(program_name)
            self.load_programTable() 


# STUDENT FUNCTIONS
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
        self.load_studentTable()

        self.studentTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.studentTable.customContextMenuRequested.connect(self.show_contextMenu)

        student_Layout.addWidget(self.studentTable)
        self.setLayout(student_Layout)

    def load_studentTable(self):
        students = get_all_students()
        self.studentTable.setRowCount(len(students))
        for row_no, student in enumerate(students):
            self.studentTable.setItem(row_no, 0, QTableWidgetItem(str(student["id"])))
            self.studentTable.setItem(row_no, 1, QTableWidgetItem(student["student_id"]))
            self.studentTable.setItem(row_no, 2, QTableWidgetItem(student["first_name"]))
            self.studentTable.setItem(row_no, 3, QTableWidgetItem(student["last_name"]))
            self.studentTable.setItem(row_no, 4, QTableWidgetItem(student["gender"]))
            self.studentTable.setItem(row_no, 5, QTableWidgetItem(str(student["year"])))
            self.studentTable.setItem(row_no, 6, QTableWidgetItem(student["program_code"]))

            program_value = student["program_code"]
            display_program = program_value if program_value else "N/A"

            self.studentTable.setItem(row_no, 6, QTableWidgetItem(display_program))
        
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
        row = self.studentTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a student to edit.")
            return 
        student_id = self.studentTable.item(row, 0).text()
        dialog = EditStudentDialog(student_id, self)
        dialog.student_updated.connect(self.load_studentTable)
        dialog.exec()

    def handle_delete(self):
        row = self.studentTable.currentRow()
        student_id = self.studentTable.item(row, 1).text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete student with ID {student_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            delete_students(student_id)
            self.load_studentTable() 