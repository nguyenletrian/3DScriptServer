from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

from .navigation import Navigation
from .pages.login import LoginPage
from .pages.register import RegisterPage
from .pages.dashboard import DashboardPage
from .builders.page_builder import build_pages
from ..api.auth import logout as api_logout
from .. import session


class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConnectVBS")
        self.resize(900, 600)
        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        self.navigation = Navigation()
        self.pages = QStackedWidget()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.dashboard_page = DashboardPage()
        self.dynamic_pages = build_pages("apps", "users")
        self.apps_page = self.dynamic_pages["apps"]
        self.users_page = self.dynamic_pages["users"]

        for page in (self.login_page, self.register_page, self.dashboard_page, *self.dynamic_pages.values()):
            self.pages.addWidget(page)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.navigation)
        main_layout.addWidget(self.pages)
        self.navigation.login_clicked.connect(lambda: self.show_page(self.login_page))
        self.navigation.register_clicked.connect(lambda: self.show_page(self.register_page))
        self.navigation.dashboard_clicked.connect(lambda: self.show_page(self.dashboard_page))
        self.navigation.apps_clicked.connect(lambda: self.show_page(self.apps_page))
        self.navigation.users_clicked.connect(lambda: self.show_page(self.users_page))
        self.navigation.logout_clicked.connect(self.logout)
        self.login_page.login_success.connect(self.refresh_ui)
        self.register_page.register_success.connect(self.handle_register_success)

    def show_page(self, page):
        self.pages.setCurrentWidget(page)
        if hasattr(page, "on_show"):
            page.on_show()

    def refresh_ui(self):
        user = session.get_user()
        self.navigation.update(user)
        self.show_page(self.dashboard_page if user else self.login_page)

    def logout(self):
        api_logout()
        session.clear_user()
        self.refresh_ui()

    def handle_register_success(self):
        username = self.register_page.username_edit.text()
        self.register_page.password_edit.clear()
        self.register_page.confirm_password_edit.clear()
        self.login_page.username_edit.setText(username)
        self.show_page(self.login_page)
