from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QMessageBox

from .navigation import Navigation
from .pages.login import LoginPage
from .pages.register.page import RegisterPage
from .pages.dashboard import DashboardPage
from .builders.page_builder import build_pages
from .runtimes.coffee import CoffeeRuntime
from ..api.auth import logout as api_logout
from .. import session


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConnectVBS")
        self.resize(900, 600)
        self.coffee_runtime = None
        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        self.navigation = Navigation()
        self.pages = QStackedWidget()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.dashboard_page = DashboardPage()
        self.dynamic_pages = build_pages("applications", "users")
        self.dynamic_pages["applications"].set_activate_callback(self.handle_application_activated)
        for page in (self.login_page, self.register_page, self.dashboard_page, *self.dynamic_pages.values()): self.pages.addWidget(page)
        main_layout = QHBoxLayout(self); main_layout.addWidget(self.navigation); main_layout.addWidget(self.pages, 1)
        self.navigation.page_clicked.connect(self.show_page); self.navigation.logout_clicked.connect(self.logout)
        self.login_page.login_success.connect(self.refresh_ui); self.register_page.register_success.connect(self.handle_register_success)

    def show_page(self, name):
        pages = {"login": self.login_page, "register": self.register_page, "dashboard": self.dashboard_page, **self.dynamic_pages}
        if self.coffee_runtime: pages["coffee"] = self.coffee_runtime
        page = pages.get(name)
        if page:
            self.pages.setCurrentWidget(page)
            if hasattr(page, "on_show"): page.on_show()
            elif hasattr(page, "refresh"): page.refresh()

    def handle_application_activated(self, result):
        instance = (result or {}).get("application_instance") or {}
        if not instance:
            QMessageBox.warning(self, "Activation", "Application activation returned no instance.")
            return
        short_name = str(instance.get("short_name", ""))
        if not short_name.startswith("coffee_"):
            QMessageBox.information(self, "Activation", f"{instance.get('name', 'Application')} activated successfully.")
            return
        if self.coffee_runtime:
            self.pages.removeWidget(self.coffee_runtime); self.coffee_runtime.deleteLater()
        self.coffee_runtime = CoffeeRuntime(instance, self); self.pages.addWidget(self.coffee_runtime)
        self.show_page("coffee"); self.coffee_runtime.show_page("coffee_dashboard")

    def refresh_ui(self):
        user = session.get_user(); self.navigation.update(user); self.show_page("dashboard" if user else "login")

    def logout(self):
        api_logout(); session.clear_user()
        if self.coffee_runtime:
            self.pages.removeWidget(self.coffee_runtime); self.coffee_runtime.deleteLater(); self.coffee_runtime = None
        self.refresh_ui()

    def handle_register_success(self):
        username = self.register_page.username_edit.text(); self.register_page.password_edit.clear(); self.register_page.confirm_password_edit.clear(); self.login_page.username_edit.setText(username); self.show_page("login")
