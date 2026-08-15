from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from .pages.dashboard import DashboardPage
from .pages.apps import AppsPage

from .. import session


class MainWindow(QWidget):

    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("ConnectVBS")
        self.resize(900, 600)

        self.setup_ui()

    def setup_ui(self):

        # =========================
        # Navigation
        # =========================

        self.dashboard_button = QPushButton(
            "Dashboard"
        )

        self.users_button = QPushButton(
            "Users"
        )
        user = session.get_user()
        if not user or user.get("role") != "admin":
            self.users_button.hide()


        self.apps_button = QPushButton(
            "Apps"
        )

        self.settings_button = QPushButton(
            "Settings"
        )

        self.logout_button = QPushButton(
            "Logout"
        )

        navigation_layout = QVBoxLayout()

        navigation_layout.addWidget(
            self.dashboard_button
        )

        navigation_layout.addWidget(
            self.users_button
        )

        navigation_layout.addWidget(
            self.apps_button
        )

        navigation_layout.addWidget(
            self.settings_button
        )

        navigation_layout.addStretch()

        navigation_layout.addWidget(
            self.logout_button
        )

        # =========================
        # Pages
        # =========================

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()       

        self.pages.addWidget(
            self.dashboard_page
        )

        self.apps_page = AppsPage()
        self.pages.addWidget(
            self.apps_page
        )


        # =========================
        # Main Layout
        # =========================

        main_layout = QHBoxLayout(self)

        main_layout.addLayout(
            navigation_layout
        )

        main_layout.addWidget(
            self.pages
        )

        # =========================
        # Signals
        # =========================

        self.dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.dashboard_page
            )
        )

        self.apps_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.apps_page
            )
        )
        

        self.logout_button.clicked.connect(
            self.handle_logout
        )

    def handle_logout(self):

        session.clear_user()

        self.close()

        self.login_window.password_edit.clear()
        self.login_window.error_label.clear()

        self.login_window.show()