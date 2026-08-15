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

        title = QLabel("Dashboard")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        self.welcome_label = QLabel()

        self.welcome_label.setStyleSheet(
            "font-size: 16px;"
        )

        layout = QVBoxLayout(self)

        layout.addWidget(title)
        layout.addWidget(
            self.welcome_label
        )

        layout.addStretch()

        self.refresh()

    def refresh(self):

        user = session.get_user()

        username = (
            user["username"]
            if user
            else "Unknown"
        )

        self.welcome_label.setText(
            f"Welcome, {username}"
        )