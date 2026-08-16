from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from ...api.apps import get_apps, create_app


class AppsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)

        title = QLabel("Apps")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("App name")
        self.main_layout.addWidget(self.name_edit)

        self.create_button = QPushButton("Create App")
        self.main_layout.addWidget(self.create_button)
        self.create_button.clicked.connect(self.create_app)

        self.apps_layout = QVBoxLayout()
        self.main_layout.addLayout(self.apps_layout)

        self.main_layout.addStretch()

    def on_show(self):
        self.load_apps()

    def load_apps(self):
        while self.apps_layout.count():
            item = self.apps_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        try:
            result = get_apps()
        except Exception as e:
            self.apps_layout.addWidget(QLabel(f"Failed to load apps: {e}"))
            return

        if not result.get("success"):
            return

        for app in result.get("apps", []):
            self.apps_layout.addWidget(QLabel(f'{app["id"]} | ' f'{app["name"]}'))

    def create_app(self):
        name = self.name_edit.text().strip()

        if not name:
            return

        try:
            result = create_app(name)
        except Exception as e:
            self.apps_layout.addWidget(QLabel(f"Failed to create app: {e}"))
            return

        if not result.get("success"):
            return

        self.name_edit.clear()
        self.load_apps()