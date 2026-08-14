import sys

from PySide6.QtWidgets import QApplication

from .ui.login import LoginWindow


def main():

    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())