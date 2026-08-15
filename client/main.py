import sys
from PySide6.QtWidgets import QApplication
from .ui.login import LoginWindow

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())