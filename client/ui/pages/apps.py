from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ...api import get_apps


class AppsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Apps")

        self.layout.addWidget(
            self.title
        )

        self.load_apps()

    def load_apps(self):

        try:
            result = get_apps()

        except Exception as e:
            self.layout.addWidget(
                QLabel(
                    f"Failed to load apps: {e}"
                )
            )
            return

        if not result.get("success"):
            return

        for app in result.get("apps", []):

            name = QLabel(
                app["name"]
            )

            description = QLabel(
                app["description"]
            )

            self.layout.addWidget(name)
            self.layout.addWidget(description)