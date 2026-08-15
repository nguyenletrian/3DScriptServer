from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class UsersPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        title = QLabel("Users")

        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        layout = QVBoxLayout(self)

        layout.addWidget(title)

        layout.addStretch()