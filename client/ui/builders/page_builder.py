import importlib

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

from .form_builder import FormBuilder
from .list_builder import ListBuilder


class PageBuilder(QWidget):

    def __init__(self, config, parent=None):
        super().__init__(parent)

        self.config = config or {}
        self.functions = self._load_functions()
        self.editing_id = None
        self.form = None
        self.list = None

        self.setup_ui()

    def _load_functions(self):
        module_name = self.__class__.__module__.rsplit(".", 1)[0] + ".functions"
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            return None

    def _get_function(self, name):
        if not self.functions or not name:
            return None
        return getattr(self.functions, name, None)

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self._build_header()
        self._build_form()
        self._build_list()
        self.layout.addStretch()

    def _build_header(self):
        header = QHBoxLayout()
        title = self.config.get("title")

        if title:
            label = QLabel(title)
            label.setStyleSheet("font-size: 24px; font-weight: bold;")
            header.addWidget(label)

        header.addStretch()

        button_config = self.config.get("add_button")
        if button_config:
            self.add_button = QPushButton(button_config.get("text", "Add"))
            self.add_button.clicked.connect(self.add_item)
            header.addWidget(self.add_button)

        self.layout.addLayout(header)

    def _build_form(self):
        config = self.config.get("form")
        if not config:
            return

        self.form = FormBuilder(
            config.get("fields", {}),
            config.get("submit_text", "Submit"),
        )
        self.form.set_submit_callback(self.submit_form)
        self.layout.addWidget(self.form)

    def _build_list(self):
        config = self.config.get("list")
        if not config:
            return

        self.list = ListBuilder(
            config.get("columns", []),
            config.get("actions", []),
        )
        self.list.set_edit_callback(self.edit_item)
        self.list.set_delete_callback(self.delete_item)
        self.layout.addWidget(self.list)

    def on_show(self):
        loader = self._get_function(
            self.config.get("data", {}).get("loader")
        )
        if loader:
            loader(self)

    def set_data(self, data):
        if self.list:
            self.list.set_data(data)

    def set_form_data(self, data):
        if self.form:
            self.form.set_data(data)

    def get_form_data(self):
        return self.form.get_data() if self.form else {}

    def clear_form(self):
        if self.form:
            self.form.clear()

    def add_item(self):
        self.editing_id = None
        self.clear_form()
        if self.form:
            self.form.submit_button.setText(
                self.config.get("form", {}).get("submit_text", "Submit")
            )

    def edit_item(self, item):
        self.editing_id = item.get("id")
        self.set_form_data(item)
        if self.form:
            self.form.submit_button.setText(
                self.config.get("form", {}).get("edit_submit_text", "Update")
            )

    def delete_item(self, item):
        function = self._get_function(
            self.config.get("data", {}).get("deleter")
        )
        if function:
            function(self, item.get("id"))

    def submit_form(self, data):
        data_config = self.config.get("data", {})
        name = "updater" if self.editing_id else "creator"
        function = self._get_function(data_config.get(name))

        if function:
            if self.editing_id:
                function(self, self.editing_id, data)
            else:
                function(self, data)
