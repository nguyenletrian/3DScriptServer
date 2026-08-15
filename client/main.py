import sys

from PySide6.QtWidgets import QApplication

from .ui.app import AppWindow


def main():

    app = QApplication(sys.argv)

    window = AppWindow()

    window.show()

    sys.exit(
        app.exec()
    )