from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton


class ListBuilder(QWidget):
    def __init__(self, columns, actions=None, parent=None):
        super().__init__(parent)
        self.columns = columns or []
        self.actions = actions or []
        self.items = []
        self.edit_callback = self.delete_callback = self.activate_callback = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)

    def set_data(self, items):
        self.clear()
        self.items = items or []
        for item in self.items:
            self._add_row(item)

    def _add_row(self, item):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        for column in self.columns:
            name = column if isinstance(column, str) else column["name"]
            label = name if isinstance(column, str) else column.get("label", name)
            widget = QLabel(str(item.get(name, "")))
            widget.setToolTip(label)
            layout.addWidget(widget)
        layout.addStretch()
        if "activate" in self.actions:
            button = QPushButton("Activate")
            button.clicked.connect(lambda checked=False, data=item: self._activate(data))
            layout.addWidget(button)
        if "edit" in self.actions:
            button = QPushButton("Edit")
            button.clicked.connect(lambda checked=False, data=item: self._edit(data))
            layout.addWidget(button)
        if "delete" in self.actions:
            button = QPushButton("Delete")
            button.clicked.connect(lambda checked=False, data=item: self._delete(data))
            layout.addWidget(button)
        self.layout.addWidget(row)

    def _activate(self, item):
        if self.activate_callback:
            self.activate_callback(item)

    def _edit(self, item):
        if self.edit_callback:
            self.edit_callback(item)

    def _delete(self, item):
        if self.delete_callback:
            self.delete_callback(item)

    def set_activate_callback(self, callback): self.activate_callback = callback
    def set_edit_callback(self, callback): self.edit_callback = callback
    def set_delete_callback(self, callback): self.delete_callback = callback

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()
        self.items = []
