from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,)
from ...api.auth import register

class RegisterPage(QWidget):
    register_success = Signal()
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Register")
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Confirm password")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register")

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")


        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.confirm_password_edit)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)
        layout.addStretch()
        self.register_button.clicked.connect(self.handle_register)

    def handle_register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = (self.confirm_password_edit.text())
        self.error_label.clear()

        if not username or not password:
            self.error_label.setText("Please enter username and password.")
            return

        if password != confirm_password:
            self.error_label.setText("Passwords do not match.")
            return

        try:
            result = register(username,password,)
        except Exception as e:
            self.error_label.setText(f"Connection error: {e}")
            return

        if not result.get("success"):
            self.error_label.setText(result.get("message","Registration failed."))
            return

        self.register_success.emit()