import sys
from PySide6.QtWidgets import QApplication
from GUI.WindowMain import mainApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainApp()
    sys.exit(app.exec())