import os

from PySide6.QtWidgets import ( 
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget 
    )
from PySide6.QtGui import QIcon, QAction
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

        #Layout for the table pages
        self.TablePage = QStackedWidget()
        self.TablePage.setMinimumHeight(580)

        self.TablePage.addWidget((StudentsTable()))
        self.TablePage.addWidget((ProgramTable()))
        self.TablePage.addWidget((CollegeTable()))

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
    

    # Makes sure add pop up Dialog opens when button clicked
    def Add_popup(self):
        dialog_index = self.TablePage.currentIndex()
        if dialog_index == 0:
            self.addDialog_Student()
        elif dialog_index == 1:
            self.addDialog_Program()
        elif dialog_index == 2:
            self.addDialog_College()

    def addDialog_Student(self):
        dialogStudent = AddStudentsDialog(self)
        dialogStudent.exec()
    def addDialog_Program(self):
        dialogProgram = AddProgramDialog(self)
        dialogProgram.exec()   
    def addDialog_College(self):
        dialogCollege = AddCollegeDialog(self)
        dialogCollege.exec()








