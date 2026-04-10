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
        self.collegeTable.setColumnCount(2)
        self.collegeTable.setHorizontalHeaderLabels(["College Name", "College Code"])
        self.collegeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_collegeTable()

        self.collegeTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.collegeTable.customContextMenuRequested.connect(self.show_contextMenu)

        college_Layout.addWidget(self.collegeTable)
        self.setLayout(college_Layout)

    def load_collegeTable(self):
        colleges = get_all_college()
        self.collegeTable.setRowCount(len(colleges))
        for row_no, college in enumerate(colleges):
            name_item = QTableWidgetItem(college["college_name"])
            name_item.setData(Qt.UserRole, college["id"])
            self.collegeTable.setItem(row_no, 0, name_item)
            self.collegeTable.setItem(row_no, 1, QTableWidgetItem(college["college_code"]))

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
 
        college_id   = self.collegeTable.item(row, 0).data(Qt.UserRole)
        college_name = self.collegeTable.item(row, 0).text()
        college_code = self.collegeTable.item(row, 1).text()
 
        dialog = EditCollegeDialog(college_id, college_name, college_code, self)
        dialog.college_updated.connect(self.load_collegeTable)
        dialog.exec()

    def handle_delete(self):
        row = self.collegeTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a college to delete.")
            return
 
        college_id   = self.collegeTable.item(row, 0).data(Qt.UserRole)
        college_name = self.collegeTable.item(row, 0).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{college_name}'?\n\n"
            "Warning: This will also delete all associated Programs and "
            "unassign Students!",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_college(college_id)
            self.load_collegeTable()


# PROGRAM FUNCTIONS
class ProgramTable(QWidget):
    def __init__(self):
        super().__init__()
        self.programtable_setup()

    def programtable_setup(self):
        program_Layout = QVBoxLayout()

        self.programTable = QTableWidget()
        self.programTable.setColumnCount(3)
        self.programTable.setHorizontalHeaderLabels(["Program Code", "Program Name", "College ID"])
        self.programTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_programTable()

        self.programTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.programTable.customContextMenuRequested.connect(self.show_contextMenu)

        program_Layout.addWidget(self.programTable)
        self.setLayout(program_Layout)

    def load_programTable(self):
        programs = get_all_program()
        self.programTable.setRowCount(len(programs))
        for row_no, program in enumerate(programs):
            code_item = QTableWidgetItem(program["program_code"])
            code_item.setData(Qt.UserRole, program["id"])   # store real DB id
            self.programTable.setItem(row_no, 0, code_item)
            self.programTable.setItem(row_no, 1, QTableWidgetItem(program["program_name"]))
            self.programTable.setItem(row_no, 2, QTableWidgetItem(str(program["college_code"])))

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
 
        program_id   = self.programTable.item(row, 0).data(Qt.UserRole)
        program_code = self.programTable.item(row, 0).text()
        program_name = self.programTable.item(row, 1).text()
        college_code = self.programTable.item(row, 2).text()
 
        dialog = EditProgramDialog(program_id, program_name, program_code, college_code, self)
        dialog.program_updated.connect(self.load_programTable)
        dialog.exec()

    def handle_delete(self):
        row = self.programTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a program to delete.")
            return
 
        program_id   = self.programTable.item(row, 0).data(Qt.UserRole)
        program_name = self.programTable.item(row, 1).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{program_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_program(program_id)
            self.load_programTable()


# STUDENT FUNCTIONS
class StudentsTable(QWidget):
    def __init__(self ):
        super().__init__()
        self.studentstable_setup()

    def studentstable_setup(self):
        student_Layout = QVBoxLayout()

        self.studentTable = QTableWidget()
        self.studentTable.setColumnCount(6)
        self.studentTable.setHorizontalHeaderLabels(["Student ID", "First Name", "Last Name", "Gender", "Year", "Program"])
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
            sid_item = QTableWidgetItem(student["student_id"])
            sid_item.setData(Qt.UserRole, student["id"])    # store real DB id
            self.studentTable.setItem(row_no, 0, sid_item)
            self.studentTable.setItem(row_no, 1, QTableWidgetItem(student["first_name"]))
            self.studentTable.setItem(row_no, 2, QTableWidgetItem(student["last_name"]))
            self.studentTable.setItem(row_no, 3, QTableWidgetItem(student["gender"]))
            self.studentTable.setItem(row_no, 4, QTableWidgetItem(str(student["year"])))
            program_value = student["program_code"] or "N/A"
            self.studentTable.setItem(row_no, 5, QTableWidgetItem(program_value))
        
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
 
        db_id      = self.studentTable.item(row, 0).data(Qt.UserRole)  # real DB id
        student_data = {
            "student_id":   self.studentTable.item(row, 0).text(),
            "first_name":   self.studentTable.item(row, 1).text(),
            "last_name":    self.studentTable.item(row, 2).text(),
            "gender":       self.studentTable.item(row, 3).text(),
            "year":         self.studentTable.item(row, 4).text(),
            "program_code": self.studentTable.item(row, 5).text(),
        }
 
        dialog = EditStudentDialog(db_id, student_data, self)
        dialog.student_updated.connect(self.load_studentTable)
        dialog.exec()


    def handle_delete(self):
        row = self.studentTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a student to delete.")
            return
 
        db_id      = self.studentTable.item(row, 0).data(Qt.UserRole)
        student_id = self.studentTable.item(row, 0).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student '{student_id}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_students(db_id)
            self.load_studentTable() 