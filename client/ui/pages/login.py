from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from ...api.auth import login
from ... import session


class LoginPage(QWidget):

    login_success = Signal()

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.username_label = QLabel("Username")

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText(
            "Enter username"
        )

        self.password_label = QLabel("Password")

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText(
            "Enter password"
        )

        self.password_edit.setEchoMode(
            QLineEdit.Password
        )

        self.login_button = QPushButton("Login")

        self.error_label = QLabel()
        self.error_label.setStyleSheet(
            "color: red;"
        )

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.username_label
        )

        layout.addWidget(
            self.username_edit
        )

        layout.addWidget(
            self.password_label
        )

        layout.addWidget(
            self.password_edit
        )

        layout.addWidget(
            self.login_button
        )

        layout.addWidget(
            self.error_label
        )

        layout.addStretch()

        self.login_button.clicked.connect(
            self.handle_login
        )

    def handle_login(self):

        username = self.username_edit.text()
        password = self.password_edit.text()

        self.error_label.clear()

        if not username or not password:

            self.error_label.setText(
                "Please enter username and password."
            )

            return

        try:

            result = login(
                username,
                password,
            )

        except Exception as e:

            self.error_label.setText(
                f"Connection error: {e}"
            )

            return

        if not result.get("success"):

            self.error_label.setText(
                result.get(
                    "message",
                    "Invalid username or password.",
                )
            )

            return

        session.set_user(
            result["user"]
        )

        self.login_success.emit()