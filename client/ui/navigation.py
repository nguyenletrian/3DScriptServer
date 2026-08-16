from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout


NAV_CONFIG = [
    {"name": "login", "title": "Login", "guest": True},
    {"name": "register", "title": "Register", "guest": True},
    {"name": "dashboard", "title": "Dashboard", "auth": True},
    {"name": "apps", "title": "Apps", "auth": True},
    {"name": "users", "title": "Users", "role": "admin"},
]


class Navigation(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        for item in NAV_CONFIG:
            button = QPushButton(item["title"])
            button.clicked.connect(lambda _, name=item["name"]: self.page_clicked.emit(name))
            self.buttons[item["name"]] = button
            layout.addWidget(button)
        layout.addStretch()
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

    def update(self, user):
        logged_in = user is not None
        for item in NAV_CONFIG:
            visible = (not logged_in) if item.get("guest") else item.get("auth", False) and logged_in
            if item.get("role"):
                visible = logged_in and user.get("role") == item["role"]
            self.buttons[item["name"]].setVisible(visible)
        self.logout_button.setVisible(logged_in)

    def logout(self):
        self.page_clicked.emit("logout")
