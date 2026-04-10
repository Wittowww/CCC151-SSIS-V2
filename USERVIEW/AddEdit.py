from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QComboBox, QMessageBox
)
from PySide6.QtCore import Signal

from DATA.Commands import (
    add_college, update_college, get_all_college,
    add_program, update_program, get_all_program,
    add_students, update_students, get_all_students
)


# COLLEGE DIALOG
class AddCollegeDialog(QDialog):
    college_updated = Signal()

    def __init__(self,  parent = None):
        super().__init__(parent)
        self.setWindowTitle("Add College")
        self.setFixedSize(500, 200)

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
        
        saveButton = QPushButton("Add College")
        saveButton.clicked.connect(self.save_college)
        college_layout.addWidget(saveButton)

        self.setLayout(college_layout)

    def validate_college(self):
        if not self.Input_collegeName.text().strip():
            return "College Name is required"
        if not self.Input_collegeCode.text().strip():
            return "College Code is required"
        return None

    def save_college(self):
        error =self.validate_college()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
                   
        try:
            add_college(
                self.Input_collegeName.text().strip(),
                self.Input_collegeCode.text().strip()
            )

            self.college_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

class EditCollegeDialog(QDialog):
    college_updated = Signal()

    def __init__(self, college_id,college_name = "", college_code = "", parent = None):
        super().__init__(parent)
        self.setWindowTitle("Edit College")
        self.setFixedSize(500, 200)

        self.college_id = college_id
        self.collegeUI_setup(college_name, college_code)

    def collegeUI_setup(self, college_name, college_code):
        college_layout = QVBoxLayout()
        college_form   = QFormLayout()
 
        self.Input_collegeName = QLineEdit(college_name)
        self.Input_collegeCode = QLineEdit(college_code)
 
        college_form.addRow("College Name:", self.Input_collegeName)
        college_form.addRow("College Code:", self.Input_collegeCode)
        college_layout.addLayout(college_form)
 
        saveButton = QPushButton("Save Changes")
        saveButton.clicked.connect(self._save)
        college_layout.addWidget(saveButton)
 
        self.setLayout(college_layout)

    def _validate(self):
        if not self.Input_collegeName.text().strip():
            return "College Name is required."
        if not self.Input_collegeCode.text().strip():
            return "College Code is required."
        return None

    def _save(self):
        error = self._validate()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        try:
            update_college(
                self.college_id,
                self.Input_collegeName.text().strip(),
                self.Input_collegeCode.text().strip()
            )
            self.college_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

# PROGRAM DIALOG
class AddProgramDialog(QDialog):
    program_updated = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Add Program")
        self.setFixedSize(500, 200)

        self.programUI_setup()

    def programUI_setup(self):
        layout = QVBoxLayout()
        form   = QFormLayout()
 
        self.Input_programName = QLineEdit()
        self.Input_programCode = QLineEdit()
 
        self.Choose_college = QComboBox()
        for c in get_all_college():
            self.Choose_college.addItem(c["college_code"], c["college_code"])
 
        form.addRow("Program Name:", self.Input_programName)
        form.addRow("Program Code:", self.Input_programCode)
        form.addRow("College:",      self.Choose_college)
        layout.addLayout(form)
 
        save_btn = QPushButton("Add Program")
        save_btn.clicked.connect(self._save)
        layout.addWidget(save_btn)
 
        self.setLayout(layout)

    def _validate(self):
        if not self.Input_programName.text().strip():
            return "Program Name is required."
        if not self.Input_programCode.text().strip():
            return "Program Code is required."
        if self.Choose_college.count() == 0:
            return "No colleges available. Please add a college first."
        return None
 
    def _save(self):
        error = self._validate()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        try:
            add_program(
                self.Input_programCode.text().strip(),
                self.Input_programName.text().strip(),
                self.Choose_college.currentData()
            )
            self.program_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

class EditProgramDialog(QDialog):
    program_updated = Signal()
 
    def __init__(self, program_id, program_name = "", program_code = "", college_code = "", parent = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Program")
        self.setFixedSize(500, 200)

        self.program_id = program_id
        self._build_ui(program_name, program_code, college_code)
 
    def _build_ui(self, program_name, program_code, college_code):
        program_layout = QVBoxLayout()
        program_form   = QFormLayout()
 
        self.Input_programName = QLineEdit(program_name)
        self.Input_programCode = QLineEdit(program_code)
 
        self.Choose_college = QComboBox()
        for c in get_all_college():
            self.Choose_college.addItem(c["college_code"], c["college_code"])
 
        # Pre-select the current college
        idx = self.Choose_college.findData(college_code)
        if idx >= 0:
            self.Choose_college.setCurrentIndex(idx)
 
        program_form.addRow("Program Name:", self.Input_programName)
        program_form.addRow("Program Code:", self.Input_programCode)
        program_form.addRow("College:",      self.Choose_college)
        program_layout.addLayout(program_form)
 
        saveButton = QPushButton("Save Changes")
        saveButton.clicked.connect(self._save)
        program_layout.addWidget(saveButton)
 
        self.setLayout(program_layout)
 
    def _validate(self):
        if not self.Input_programName.text().strip():
            return "Program Name is required."
        if not self.Input_programCode.text().strip():
            return "Program Code is required."
        return None
 
    def _save(self):
        error = self._validate()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        try:
            update_program(
                self.Input_programName.text().strip(),
                self.Input_programCode.text().strip(),
                self.Choose_college.currentData(),
                self.program_id
            )
            self.program_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

# STUDENT DIALOG
class AddStudentsDialog(QDialog):
    student_updated = Signal()
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")
        self.setFixedSize(500, 200)

        self._build_ui()
 
    def _build_ui(self):
        student_layout = QVBoxLayout()
        student_form   = QFormLayout()
 
        self.Input_studentID  = QLineEdit()
        self.Input_firstName  = QLineEdit()
        self.Input_lastName   = QLineEdit()
 
        self.Choose_gender = QComboBox()
        self.Choose_gender.addItems(["Select Gender", "Female", "Male"])
 
        self.Input_year = QLineEdit()
 
        self.Choose_program = QComboBox()
        for p in get_all_program():
            self.Choose_program.addItem(p["program_code"], p["program_code"])
 
        student_form.addRow("Student ID:", self.Input_studentID)
        student_form.addRow("First Name:", self.Input_firstName)
        student_form.addRow("Last Name:",  self.Input_lastName)
        student_form.addRow("Gender:",     self.Choose_gender)
        student_form.addRow("Year:",       self.Input_year)
        student_form.addRow("Program:",    self.Choose_program)
        student_layout.addLayout(student_form)
 
        saveButton = QPushButton("Add Student")
        saveButton.clicked.connect(self._save)
        student_layout.addWidget(saveButton)
 
        self.setLayout(student_layout)
 
    def _validate(self):
        if not self.Input_studentID.text().strip():
            return "Student ID is required."
        if not self.Input_firstName.text().strip():
            return "First Name is required."
        if not self.Input_lastName.text().strip():
            return "Last Name is required."
        if self.Choose_gender.currentText() == "Select Gender":
            return "Please select a gender."
        if not self.Input_year.text().strip().isdigit():
            return "Year must be a valid number."
        if self.Choose_program.count() == 0:
            return "No programs available. Please add a program first."
        return None
 
    def _save(self):
        error = self._validate()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        try:
            add_students(
                self.Input_studentID.text().strip(),
                self.Input_firstName.text().strip(),
                self.Input_lastName.text().strip(),
                self.Choose_gender.currentText(),
                int(self.Input_year.text().strip()),
                self.Choose_program.currentData()
            )
            self.student_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

class EditStudentDialog(QDialog):
    student_updated = Signal()
 
    def __init__(self, student_id, student_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.setFixedSize(500, 200)

        self.student_id = student_id
        self._build_ui(student_data or {})
 
    def _build_ui(self, d):
        student_layout = QVBoxLayout()
        student_form   = QFormLayout()
 
        self.Input_studentID = QLineEdit(d.get("student_id", ""))
        self.Input_firstName = QLineEdit(d.get("first_name", ""))
        self.Input_lastName  = QLineEdit(d.get("last_name",  ""))
 
        self.Choose_gender = QComboBox()
        self.Choose_gender.addItems(["Select Gender", "Female", "Male"])
        idx = self.Choose_gender.findText(d.get("gender", ""))
        if idx >= 0:
            self.Choose_gender.setCurrentIndex(idx)
 
        self.Input_year = QLineEdit(str(d.get("year", "")))
 
        self.Choose_program = QComboBox()
        for p in get_all_program():
            self.Choose_program.addItem(p["program_code"], p["program_code"])
        pidx = self.Choose_program.findData(d.get("program_code", ""))
        if pidx >= 0:
            self.Choose_program.setCurrentIndex(pidx)
 
        student_form.addRow("Student ID:", self.Input_studentID)
        student_form.addRow("First Name:", self.Input_firstName)
        student_form.addRow("Last Name:",  self.Input_lastName)
        student_form.addRow("Gender:",     self.Choose_gender)
        student_form.addRow("Year:",       self.Input_year)
        student_form.addRow("Program:",    self.Choose_program)
        student_layout.addLayout(student_form)
 
        saveButton = QPushButton("Save Changes")
        saveButton.clicked.connect(self._save)
        student_layout.addWidget(saveButton)
 
        self.setLayout(student_layout)
 
    def _validate(self):
        if not self.Input_studentID.text().strip():
            return "Student ID is required."
        if not self.Input_firstName.text().strip():
            return "First Name is required."
        if not self.Input_lastName.text().strip():
            return "Last Name is required."
        if self.Choose_gender.currentText() == "Select Gender":
            return "Please select a gender."
        if not self.Input_year.text().strip().isdigit():
            return "Year must be a valid number."
        return None
 
    def _save(self):
        error = self._validate()
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        try:
            update_students(
                self.Input_studentID.text().strip(),
                self.Input_firstName.text().strip(),
                self.Input_lastName.text().strip(),
                self.Choose_gender.currentText(),
                int(self.Input_year.text().strip()),
                self.Choose_program.currentData(),
                self.student_id
            )
            self.student_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")
