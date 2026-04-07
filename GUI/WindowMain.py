import os

from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget )
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from USERVIEW.DataTable import StudentsTable
from USERVIEW.DataTable import ProgramTable
from USERVIEW.DataTable import CollegeTable


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
        #self.Students_button.clicked.connect()
        #self.Programs_button.clicked.connect()
        #self.Colleges_button.clicked.connect()

        upperBox.addStretch()

        #Layout for the table pages
        TablePage = QStackedWidget()
        TablePage.setMinimumHeight(580)


        TablePage.addWidget((StudentsTable()))
        TablePage.addWidget((ProgramTable()))
        TablePage.addWidget((CollegeTable()))

        layout_Main.addWidget(TITLElable)
        layout_Main.addWidget(upperBox_container)
        layout_Main.addWidget(TablePage)








