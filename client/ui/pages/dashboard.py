from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ... import session


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        user = session.get_user()

        username = user["username"] if user else "Unknown"

        title = QLabel("Dashboard")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        welcome = QLabel(
            f"Welcome, {username}"
        )

        welcome.setStyleSheet(
            "font-size: 16px;"
        )

        layout = QVBoxLayout(self)

        layout.addWidget(title)
        layout.addWidget(welcome)

        layout.addStretch()