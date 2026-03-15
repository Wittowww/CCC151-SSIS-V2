import os

from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, QDialog, QHBoxLayout, QVBoxLayout )
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


