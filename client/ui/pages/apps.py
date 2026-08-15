from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ...api.apps import get_apps


class AppsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        title = QLabel("Apps")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        self.layout.addWidget(title)
        self.apps_layout = QVBoxLayout()
        self.layout.addLayout(
            self.apps_layout
        )

        self.layout.addStretch()

    def on_show(self):
        self.load_apps()

    def load_apps(self):
        # Clear old apps
        while self.apps_layout.count():

            item = self.apps_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        try:

            result = get_apps()

        except Exception as e:

            self.apps_layout.addWidget(
                QLabel(
                    f"Failed to load apps: {e}"
                )
            )

            return

        if not result.get("success"):
            return

        for app in result.get("apps", []):

            self.apps_layout.addWidget(
                QLabel(
                    f'{app["id"]} | '
                    f'{app["name"]}'
                )
            )