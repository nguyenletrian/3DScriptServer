from PySide6.QtWidgets import QLayout, QLabel

# ... existing code ...

    def set_error(self, message):
        if not hasattr(self, "error_label"):
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red; border: none;")
            target = self.form_panel or self
            layout = target if isinstance(target, QLayout) else target.layout()
            if layout:
                layout.addWidget(self.error_label)
        self.error_label.setText(message or "")
