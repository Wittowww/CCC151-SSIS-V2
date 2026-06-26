import sys
import os
from PySide6.QtWidgets import QApplication
from GUI.WindowMain import mainApp

app = QApplication(sys.argv)

#style the data
qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
with open(qss_path, "r") as f:
    app.setStyleSheet(f.read())

if __name__ == "__main__":
    window = mainApp()
    sys.exit(app.exec())