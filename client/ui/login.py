from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ConnectVBS")
        self.resize(400, 250)

        self.username_label = QLabel("Username")

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter username")

        self.password_label = QLabel("Password")

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter password")
        self.password_edit.setEchoMode(
            QLineEdit.Password
        )

        self.login_button = QPushButton("Login")

        layout = QVBoxLayout(self)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)

        layout.addWidget(self.login_button)