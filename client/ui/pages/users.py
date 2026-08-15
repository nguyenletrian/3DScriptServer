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

        self.users_layout = QVBoxLayout()

        self.layout.addLayout(
            self.users_layout
        )

        self.layout.addStretch()

    def on_show(self):

        self.load_users()

    def load_users(self):

        # Clear old users
        while self.users_layout.count():

            item = self.users_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        try:

            result = get_users()

        except Exception as e:

            self.users_layout.addWidget(
                QLabel(
                    f"Failed to load users: {e}"
                )
            )

            return

        if not result.get("success"):
            return

        for user in result.get("users", []):

            self.users_layout.addWidget(
                QLabel(
                    f'{user["id"]} | '
                    f'{user["username"]} | '
                    f'{user["role"]}'
                )
            )