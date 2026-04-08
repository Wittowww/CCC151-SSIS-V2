from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QComboBox, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Signal

from DATA.Commands import (
    add_college, update_college, get_all_college,
    add_program, update_program, get_all_program,
    add_students, update_students, get_all_students
)


# COLLEGE DIALOG
class EditCollegeDialog(QDialog):
    student_updated = Signal()

    def __init__(self, college_id = None, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Edit College" if college_id else "Add College")

        self.college_updated = Signal()
        self.collegeUI_setup()

    def collegeUI_setup(self):
        college_layout = QVBoxLayout()
        college_form = QFormLayout()

        self.Input_collegeName = QLineEdit()
        self.Input_collegeCode = QLineEdit()

        #add items to dialog
        college_form.addRow("College:", self.Input_collegeName)
        college_form.addRow("College Code:", self.Input_collegeCode)

        college_layout.addLayout(college_form)
        
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.save_college)
        college_layout.addWidget(saveButton)

    def save_college(self):
        try:
            data = (
                self.Input_collegeName.text(),
                self.Input_collegeCode.text()
            )

            if self.college_internal_id:
                update_college(*data, self.college_internal_id)
            else:
                add_college(*data)

            self.college_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")



# PROGRAM DIALOG
class EditProgramDialog(QDialog):
    def __init__ (self, program_id = None, parent = None):
        super().__init__(parent)
        self.program_id = program_id
        self.setWindowTitle("Edit Program" if program_id else "Add Program")

        self.program_updated = Signal()
        self.programUI_setup()

    def programUI_setup(self):
        program_layout = QVBoxLayout()
        program_form = QFormLayout()

        self.Input_programName = QLineEdit()
        self.Input_programCode = QLineEdit()

        self.Choose_college = QComboBox()
        college = get_all_college()
        for c in college:
            self.Choose_college.addItem(c["college_code"], c["college_code"])

        #add items to dialog
        program_form.addRow("Program:", self.Input_programName)
        program_form.addRow("Program Code:", self.Input_programCode)
        program_form.addRow("College:", self.Choose_college)

        program_layout.addLayout(program_form)
        
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.save_program)
        program_layout.addWidget(saveButton)

    def save_program(self):
        try:
            data = (
                self.Input_programName.text(),
                self.Input_programCode.text(),
                self.Choose_college.currentData()
            )

            if self.program_internal_id:
                update_program(*data, self.program_internal_id)
            else:
                add_program(*data)

            self.program_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")


# STUDENT DIALOG
class EditStudentDialog(QDialog):
    def __init__ (self, student_id = None, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student" if student_id else "Add Student")

        self.student_updated = Signal()
        self.studentUI_setup()

    def studentUI_setup(self):
        student_layout = QVBoxLayout()
        student_form = QFormLayout()

        self.Input_studentID = QLineEdit()
        self.Input_firstName = QLineEdit()
        self.Input_lastName = QLineEdit()

        self.Choose_gender = QComboBox()
        self.Choose_gender.addItems(["Select Gender", "Female", "Male"])

        self.Input_year = QLineEdit()

        self.Choose_program = QComboBox()
        programs = get_all_program()
        for p in programs:
            self.Choose_program.addItem(p["program_code"], p["program_code"])

        #add items to dialog
        student_form.addRow("Student ID:", self.Input_studentID)
        student_form.addRow("First Name:", self.Input_firstName)
        student_form.addRow("Last Name:", self.Input_lastName)
        student_form.addRow("Gender:", self.Choose_gender)
        student_form.addRow("Year:", self.Input_year)
        student_form.addRow("Program:", self.Choose_program)

        student_layout.addLayout(student_form)
        
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.save_student)
        student_layout.addWidget(saveButton)

    def save_student(self):
        try:
            data = (
                self.Input_studentID.text(),
                self.Input_firstName.text(),
                self.Input_lastName.text(),
                self.Choose_gender.currentText(),
                int(self.Input_year.text()),
                self.Choose_program.currentData()
            )

            if self.student_internal_id:
                update_students(*data, self.student_internal_id)
            else:
                add_students(*data)

            self.student_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")