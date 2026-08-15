from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget,QPushButton,QVBoxLayout,)


class Navigation(QWidget):
    login_clicked = Signal()
    register_clicked = Signal()
    dashboard_clicked = Signal()
    apps_clicked = Signal()
    users_clicked = Signal()
    logout_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.dashboard_button = QPushButton("Dashboard")
        self.apps_button = QPushButton("Apps")
        self.users_button = QPushButton("Users")
        self.logout_button = QPushButton("Logout")

        layout = QVBoxLayout(self)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.apps_button)
        layout.addWidget(self.users_button)
        layout.addStretch()
        layout.addWidget(self.logout_button)


        self.login_button.clicked.connect(lambda: self.login_clicked.emit())
        self.register_button.clicked.connect(lambda: self.register_clicked.emit())
        self.dashboard_button.clicked.connect(lambda: self.dashboard_clicked.emit())
        self.apps_button.clicked.connect(lambda: self.apps_clicked.emit())
        self.users_button.clicked.connect(lambda: self.users_clicked.emit())
        self.logout_button.clicked.connect(lambda: self.logout_clicked.emit())

    def update(self, user):
        logged_in = user is not None
        self.login_button.setVisible(not logged_in)
        self.register_button.setVisible(not logged_in)
        self.dashboard_button.setVisible(logged_in)
        self.apps_button.setVisible(logged_in)
        self.users_button.setVisible(logged_in and user.get("role") == "admin")
        self.logout_button.setVisible(logged_in)