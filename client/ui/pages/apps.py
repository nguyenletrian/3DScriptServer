from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from ...api.apps import get_apps, create_app, update_app, delete_app
from ..builders.form_builder import FormBuilder


APP_FIELDS = {
    "name": {"type": "text", "label": "Name", "required": True},
    "description": {"type": "textarea", "label": "Description"},
}


class AppsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.editing_id = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.add_button = QPushButton("Add App")
        self.add_button.clicked.connect(self.add_app)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignLeft)

        self.apps_layout = QVBoxLayout()
        self.apps_layout.setSpacing(2)
        self.layout.addLayout(self.apps_layout)
        self.layout.addStretch()

        self.setup_form_panel()

    def setup_form_panel(self):
        self.form_panel = QWidget(self)
        self.form_panel.setStyleSheet(
            "background: white; border: 1px solid #ccc;"
        )

        panel_layout = QVBoxLayout(self.form_panel)

        self.form = FormBuilder(APP_FIELDS, "Create App")
        self.form.setMaximumWidth(300)
        self.form.set_submit_callback(self.save_app)
        panel_layout.addWidget(self.form, alignment=Qt.AlignHCenter)

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(self.form.submit_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.form.clear)
        buttons_layout.addWidget(self.clear_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_form)
        buttons_layout.addWidget(self.close_button)

        panel_layout.addLayout(buttons_layout)
        self.form_panel.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_form_geometry()

    def update_form_geometry(self):
        width = min(360, self.width() - 40)
        self.form_panel.setGeometry(
            (self.width() - width) // 2,
            40,
            width,
            self.form_panel.sizeHint().height(),
        )

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
            self.add_app_row(app)

    def add_app_row(self, app):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        layout.addWidget(QLabel(f'{app["id"]} | {app.get("name", "")} | {app.get("description", "")}'))

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda checked=False, app=app: self.edit_app(app))
        layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda checked=False, app_id=app["id"]: self.delete_app(app_id))
        layout.addWidget(delete_button)

        self.apps_layout.addWidget(row)

    def add_app(self):
        self.editing_id = None
        self.form.clear()
        self.form.submit_button.setText("Create App")
        self.show_form()

    def edit_app(self, app):
        self.editing_id = app["id"]
        self.form.set_data(app)
        self.form.submit_button.setText("Update App")
        self.show_form()

    def show_form(self):
        self.form_panel.adjustSize()
        self.update_form_geometry()
        self.form_panel.show()
        self.form_panel.raise_()

    def close_form(self):
        self.form.clear()
        self.editing_id = None
        self.form.submit_button.setText("Create App")
        self.form_panel.hide()

    def save_app(self, data):
        try:
            result = update_app(self.editing_id, data) if self.editing_id else create_app(data)
        except Exception as e:
            self.apps_layout.addWidget(QLabel(f"Failed to save app: {e}"))
            return

        if not result.get("success"):
            return

        self.close_form()
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