from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
)

from ...api.apps import get_apps


class AppCard(QFrame):

    def __init__(self, app):
        super().__init__()

        layout = QVBoxLayout(self)

        name = QLabel(
            app["name"]
        )

        description = QLabel(
            app["description"]
        )

        name.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        description.setWordWrap(True)

        layout.addWidget(name)
        layout.addWidget(description)


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

        self.load_apps()

        self.layout.addStretch()

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

            self.layout.addWidget(
                QLabel(
                    result.get(
                        "message",
                        "Failed to load apps.",
                    )
                )
            )

            return

        for app in result.get(
            "apps",
            [],
        ):

            self.layout.addWidget(
                AppCard(app)
            )