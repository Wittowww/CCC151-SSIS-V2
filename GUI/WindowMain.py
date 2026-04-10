import os

from PySide6.QtWidgets import ( 
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel, QPushButton, QStackedWidget, 
    QMessageBox, QLineEdit, QComboBox
    )
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Table Imports
from USERVIEW.DataTable import ( 
    StudentsTable, ProgramTable, CollegeTable
)

#Add Edut Dialog Imports
from USERVIEW.AddEdit import (
    EditStudentDialog, AddStudentsDialog,
    EditProgramDialog, AddProgramDialog,
    EditCollegeDialog, AddCollegeDialog
)


class mainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Student Information Management V2")
        self.setFixedSize(1200, 700)

        icon_path = os.path.join(BASE_DIR, "StudentInfo ICON.png")
        self.setWindowIcon(QIcon(icon_path))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_UI(central_widget)
        self.show()


    def main_UI (self, central_widget):
        layout_Main = QVBoxLayout(central_widget)

        #Label / name 
        TITLElable = QLabel("Simple System Information System")
        TITLElable.setFixedHeight(70)

        #Page Picker for Tables

        #layout thingsz
        upperBox_container = QWidget()
        upperBox_container.setFixedHeight(70)

        upperBox = QHBoxLayout(upperBox_container)

        self.Students_button = QPushButton ("Student")
        self.Programs_button = QPushButton ("Program")
        self.Colleges_button = QPushButton ("College")
        #makes sure button shows up
        upperBox.addWidget(self.Students_button)
        upperBox.addWidget(self.Programs_button)
        upperBox.addWidget(self.Colleges_button)
        #button actions
        self.Students_button.clicked.connect(self.showStudentsTable)
        self.Programs_button.clicked.connect(self.showProgramTable)
        self.Colleges_button.clicked.connect(self.showCollegeTable)

        upperBox.addStretch()

        #Seach Bar
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.setFixedWidth(200)
        self.searchBar.textChanged.connect(self.handle_search)
        upperBox.addWidget(self.searchBar)

        #Self Sort
        self.sortBox = QComboBox()
        self.sortBox.setFixedWidth(150)
        self.sortBox.currentIndexChanged.connect(self.handle_sort)
        upperBox.addWidget(self.sortBox)

        #Layout for the table pages
        self.TablePage = QStackedWidget()
        self.TablePage.setMinimumHeight(580)

        self.studentsTablePage = StudentsTable()
        self.programTablePage = ProgramTable()
        self.collegesTablePage = CollegeTable()

        self.TablePage.addWidget(self.studentsTablePage)
        self.TablePage.addWidget(self.programTablePage)
        self.TablePage.addWidget(self.collegesTablePage)

        self.TablePage.currentChanged.connect(self.update_sortBox)
        self.update_sortBox(0) 

        self.AddButton = QPushButton ("Add")
        upperBox.addWidget(self.AddButton)
        self.AddButton.clicked.connect(self.Add_popup)

        layout_Main.addWidget(TITLElable)
        layout_Main.addWidget(upperBox_container)
        layout_Main.addWidget(self.TablePage)


    # Makes sure the is shown when table buttons clicked
    def showStudentsTable(self):
        self.TablePage.setCurrentIndex(0)
    def showProgramTable(self):
        self.TablePage.setCurrentIndex(1)
    def showCollegeTable(self):
        self.TablePage.setCurrentIndex(2)

    def update_sortBox(self, index):
        self.sortBox.blockSignals(True) 
        self.sortBox.clear()
        if index == 0:
            self.sortBox.addItems(["Sort by...", "Student ID", "First Name", "Last Name", "Gender", "Year", "Program"])
        elif index == 1:
            self.sortBox.addItems(["Sort by...", "Program Code", "Program Name", "College Code"])
        elif index == 2:
            self.sortBox.addItems(["Sort by...", "College Name", "College Code"])
        self.sortBox.blockSignals(False)
        self.searchBar.clear()

    def handle_search(self, text):
        index = self.TablePage.currentIndex()
        if index == 0:
            self.studentsTablePage.search(text)
        elif index == 1:
            self.programTablePage.search(text)
        elif index == 2:
            self.collegesTablePage.search(text)

    def handle_sort(self, sort_index):
        if sort_index == 0:
            return 
        index = self.TablePage.currentIndex()
        col = sort_index - 1 
        if index == 0:
            self.studentsTablePage.sort(col)
        elif index == 1:
            self.programTablePage.sort(col)
        elif index == 2:
            self.collegesTablePage.sort(col)

    # Makes sure add pop up Dialog opens when button clicked
    def Add_popup(self):
        dialog_index = self.TablePage.currentIndex()
        if dialog_index == 0:
            self.addDialog_Student()
        elif dialog_index == 1:
            self.addDialog_Program()
        elif dialog_index == 2:
            self.addDialog_College()

    def on_student_added(self):
        QMessageBox.information(self, "Success", "Student added successfully!")
    def on_program_added(self):
        QMessageBox.information(self, "Success", "Program added successfully!")
    def on_college_added(self):
        QMessageBox.information(self, "Success", "College added successfully!")

    def addDialog_Student(self):
        dialogStudent = AddStudentsDialog(self)
        dialogStudent.student_updated.connect(self.studentsTablePage.load_studentTable)
        dialogStudent.student_updated.connect(self.on_student_added)
        dialogStudent.exec()

    def addDialog_Program(self):
        dialogProgram = AddProgramDialog(self)
        dialogProgram.program_updated.connect(self.programTablePage.load_programTable)
        dialogProgram.program_updated.connect(self.on_program_added)
        dialogProgram.exec()

    def addDialog_College(self):
        dialogCollege = AddCollegeDialog(self)
        dialogCollege.college_updated.connect(self.collegesTablePage.load_collegeTable)
        dialogCollege.college_updated.connect(self.on_college_added)
        dialogCollege.exec()