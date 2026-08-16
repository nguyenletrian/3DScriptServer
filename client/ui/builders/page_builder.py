import importlib

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

from .form_builder import FormBuilder
from .list_builder import ListBuilder


class PageBuilder(QWidget):

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config or {}
        self.api = self._load_api()
        self.editing_id = None
        self.form_panel = self.form = self.list = None
        self.setup_ui()

    def _load_api(self):
        name = self.config.get("name")
        if not name:
            return None
        try:
            return importlib.import_module(f"{__package__.rsplit('.', 1)[0]}.pages.{name}.api")
        except ModuleNotFoundError:
            return None

    def _call_api(self, action, *args):
        function = getattr(self.api, f"{action}_{self.config['name'].rstrip('s')}", None)
        if action == "get" and self.api:
            function = getattr(self.api, f"get_{self.config['name']}", None)
        return function(*args) if function else None

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self._build_header(); self._build_list(); self._build_form(); self.layout.addStretch()

    def _build_header(self):
        header = QHBoxLayout()
        if title := self.config.get("title"):
            label = QLabel(title); label.setStyleSheet("font-size: 24px; font-weight: bold;"); header.addWidget(label)
        header.addStretch()
        if button := self.config.get("add_button"):
            self.add_button = QPushButton(button.get("text", "Add")); self.add_button.clicked.connect(self.add_item); header.addWidget(self.add_button)
        self.layout.addLayout(header)

    def _build_list(self):
        config = self.config.get("list")
        if not config: return
        self.list = ListBuilder(config.get("columns", []), config.get("actions", []))
        self.list.set_edit_callback(self.edit_item); self.list.set_delete_callback(self.delete_item); self.layout.addWidget(self.list)

    def _build_form(self):
        config = self.config.get("form")
        if not config: return
        popup = config.get("popup", True)
        self.form_panel = QWidget(self); panel_layout = QVBoxLayout(self.form_panel); panel_layout.setContentsMargins(10, 10, 10, 10)
        if popup: self.form_panel.setStyleSheet("background: white; border: 1px solid #ccc;")
        self.form = FormBuilder(config.get("fields", {}), config.get("submit_text", "Submit")); self.form.setMaximumWidth(config.get("maximum_width", 300)); self.form.set_submit_callback(self.submit_form); panel_layout.addWidget(self.form, alignment=Qt.AlignHCenter)
        if popup:
            self._build_popup_buttons(panel_layout, config); self.form_panel.hide()
        else:
            self.form_panel.setStyleSheet(config.get("style", "")); panel_layout.addWidget(self.form.submit_button); self.layout.addWidget(self.form_panel, alignment=Qt.AlignHCenter)

    def _build_popup_buttons(self, layout, config):
        row = QHBoxLayout(); row.addWidget(self.form.submit_button)
        if config.get("clear_button", True): self.clear_button = QPushButton(config.get("clear_text", "Clear")); self.clear_button.clicked.connect(self.clear_form); row.addWidget(self.clear_button)
        if config.get("close_button", True): self.close_button = QPushButton(config.get("close_text", "Close")); self.close_button.clicked.connect(self.close_form); row.addWidget(self.close_button)
        layout.addLayout(row)

    def resizeEvent(self, event):
        super().resizeEvent(event); self.update_form_geometry()

    def update_form_geometry(self):
        config = self.config.get("form", {})
        if not self.form_panel or not config.get("popup", True): return
        width = min(config.get("popup_width", 360), max(100, self.width() - 40)); self.form_panel.setGeometry((self.width() - width) // 2, 40, width, self.form_panel.sizeHint().height())

    def show_form(self):
        if not self.form_panel or not self.config.get("form", {}).get("popup", True): return
        self.form_panel.adjustSize(); self.update_form_geometry(); self.form_panel.show(); self.form_panel.raise_()

    def close_form(self):
        self.clear_form(); self.editing_id = None
        if self.form: self.form.submit_button.setText(self.config.get("form", {}).get("submit_text", "Submit"))
        if self.form_panel and self.config.get("form", {}).get("popup", True): self.form_panel.hide()

    def on_show(self):
        if not self.api: return
        try:
            result = self._call_api("get")
            key = self.config.get("list", {}).get("data_key", self.config["name"])
            if result and result.get("success"): self.set_data(result.get(key, []))
        except Exception as e: self.set_error(str(e))

    def set_data(self, data):
        if self.list: self.list.set_data(data)

    def set_form_data(self, data):
        if self.form: self.form.set_data(data)

    def get_form_data(self): return self.form.get_data() if self.form else {}
    def clear_form(self):
        if self.form: self.form.clear()

    def set_error(self, message):
        if not hasattr(self, "error_label"):
            self.error_label = QLabel(); self.error_label.setStyleSheet("color: red; border: none;")
            if self.form_panel: self.form_panel.layout().addWidget(self.error_label)
        self.error_label.setText(message or "")

    def add_item(self):
        self.editing_id = None; self.clear_form()
        if self.form: self.form.submit_button.setText(self.config.get("form", {}).get("submit_text", "Submit"))
        self.show_form()

    def edit_item(self, item):
        self.editing_id = item.get("id"); self.set_form_data(item)
        if self.form: self.form.submit_button.setText(self.config.get("form", {}).get("edit_submit_text", "Update"))
        self.show_form()

    def delete_item(self, item):
        self._mutate("delete", item.get("id"))

    def submit_form(self, data):
        self._mutate("update" if self.editing_id else "create", self.editing_id, data) if self.editing_id else self._mutate("create", data)

    def _mutate(self, action, *args):
        try:
            result = self._call_api(action, *args)
            if result and result.get("success"):
                self.close_form(); self.on_show()
            elif result: self.set_error(result.get("message", "Operation failed."))
        except Exception as e: self.set_error(str(e))


def build_page(name):
    module = importlib.import_module(f"{__package__.rsplit('.', 1)[0]}.pages.{name}.page")
    return PageBuilder(module.PAGE_CONFIG)
