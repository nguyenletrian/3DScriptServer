from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QDoubleSpinBox,
    QCheckBox, QComboBox, QVBoxLayout, QPushButton,
)
from ..validation.validators import validate_required, get_validator
from ..validation.formatters import get_formatter


class FormBuilder(QWidget):
    def __init__(self, fields, submit_text="Submit", parent=None):
        super().__init__(parent)
        self.fields = fields
        self.widgets = {}
        self.errors = {}
        self.submit_callback = None
        self.setup_ui(submit_text)

    def setup_ui(self, submit_text):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        for name, config in self.fields.items():
            self._add_field(name, config)

        self.submit_button = QPushButton(submit_text)
        self.submit_button.clicked.connect(self.submit)

    def _add_field(self, name, config):
        label = QLabel(config.get("label", name))
        label.setStyleSheet("border: none;")

        self.layout.addWidget(label)

        widget = self._create_widget(config)

        error = QLabel()
        error.setStyleSheet(
            "border: none;"
            "color: red;"
        )
        error.hide()

        widget.installEventFilter(self)

        self.widgets[name] = widget
        self.errors[name] = error

        self.layout.addWidget(widget)
        self.layout.addWidget(error)

    def _create_widget(self, config):
        widget_type = config.get("type", "text")

        if widget_type == "textarea":
            return QTextEdit()

        if widget_type == "number":
            widget = QDoubleSpinBox()
            widget.setMaximum(config.get("maximum", 999999999))
            return widget

        if widget_type == "checkbox":
            return QCheckBox()

        if widget_type == "select":
            widget = QComboBox()
            widget.addItems(config.get("options", []))
            return widget

        return QLineEdit()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self._is_last_widget(obj):
                self.submit()
                return True

        return super().eventFilter(obj, event)

    def _is_last_widget(self, widget):
        widgets = list(self.widgets.values())
        return widgets and widgets[-1] is widget

    def set_data(self, data):
        for name, widget in self.widgets.items():
            if name not in data:
                continue

            value = data[name]

            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(str(value))
            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))
            else:
                widget.setValue(value)

    def get_data(self):
        data = {}

        for name, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                value = widget.isChecked()
            elif isinstance(widget, QComboBox):
                value = widget.currentText()
            elif isinstance(widget, QTextEdit):
                value = widget.toPlainText()
            elif isinstance(widget, QLineEdit):
                value = widget.text()
            else:
                value = widget.value()

            formatter = get_formatter(self.fields[name].get("formatter"))
            data[name] = formatter(value) if formatter else value

        return data

    def validate(self):
        self.clear_errors()
        data = self.get_data()
        first_error = None

        for name, config in self.fields.items():
            value = data[name]

            if config.get("required") and not validate_required(value):
                self.show_error(name, config.get("required_message", "This field is required."))
                first_error = first_error or self.widgets[name]
                continue

            validator = get_validator(config.get("validator"))

            if validator and validator(value) is not True:
                self.show_error(name, config.get("invalid_message", "Invalid value."))
                first_error = first_error or self.widgets[name]

        if first_error:
            first_error.setFocus()
            return False

        return True

    def show_error(self, name, message):
        self.errors[name].setText(message)
        self.errors[name].show()

    def clear_errors(self):
        for error in self.errors.values():
            error.clear()
            error.hide()

    def submit(self):
        if self.validate() and self.submit_callback:
            self.submit_callback(self.get_data())

    def set_submit_callback(self, callback):
        self.submit_callback = callback

    def clear(self):
        for widget in self.widgets.values():
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            else:
                widget.setValue(0)

        self.clear_errors()