from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from ...api.apps import get_apps, create_app, delete_app


class AppsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("App name")

        self.create_button = QPushButton("Create App")
        self.create_button.clicked.connect(self.create_app)

        self.layout.addWidget(QLabel("Apps"))
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.create_button)

        self.apps_layout = QVBoxLayout()
        self.apps_layout.setSpacing(2)
        self.layout.addLayout(self.apps_layout)
        self.layout.addStretch()

    def on_show(self):
        self.load_apps()

    def load_apps(self):
        while self.apps_layout.count():
            item = self.apps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            result = get_apps()
        except Exception as e:
            self.apps_layout.addWidget(QLabel(f"Failed to load apps: {e}"))
            return

        if not result.get("success"):
            return

        for app in result.get("apps", []):
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            layout.addWidget(QLabel(f'{app["id"]} | ' f'{app["name"]}'))
            button = QPushButton("Delete")
            button.clicked.connect(lambda checked=False, app_id=app["id"]: self.delete_app(app_id))
            layout.addWidget(button)
            self.apps_layout.addWidget(row)

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

    def delete_app(self, app_id):
        try:
            result = delete_app(app_id)
        except Exception as e:
            self.apps_layout.addWidget(QLabel(f"Failed to delete app: {e}"))
            return

        if not result.get("success"):
            return

        self.load_apps()