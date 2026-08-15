from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ...api.users import get_users


class UsersPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        title = QLabel("Users")

        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        self.layout.addWidget(title)

        self.load_users()

        self.layout.addStretch()

    def load_users(self):

        try:
            result = get_users()

        except Exception as e:

            self.layout.addWidget(
                QLabel(
                    f"Failed to load users: {e}"
                )
            )

            return

        if not result.get("success"):
            return

        for user in result.get("users", []):

            self.layout.addWidget(
                QLabel(
                    f'{user["id"]} | '
                    f'{user["username"]} | '
                    f'{user["role"]}'
                )
            )