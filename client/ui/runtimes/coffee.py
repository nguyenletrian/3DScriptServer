from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget

from ..builders.page_builder import build_page


class CoffeeRuntime(QWidget):
    PAGE_NAMES = [
        "coffee_dashboard",
        "coffee_products",
        "coffee_categories",
        "coffee_customers",
        "coffee_orders",
    ]

    def __init__(self, instance=None, parent=None):
        super().__init__(parent)
        self.instance = instance or {}
        self.pages = {name: build_page(name) for name in self.PAGE_NAMES}
        self.stack = QStackedWidget()
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        main = QVBoxLayout(self)
        header = QHBoxLayout()
        title = QLabel(self.instance.get("name", "Coffee"))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        back = QPushButton("Applications")
        back.clicked.connect(lambda: self.window().show_page("applications"))
        header.addWidget(back)
        main.addLayout(header)

        body = QHBoxLayout()
        nav = QVBoxLayout()
        for name, page in self.pages.items():
            title = page.config.get("title", name)
            button = QPushButton(title)
            button.clicked.connect(lambda checked=False, n=name: self.show_page(n))
            self.buttons[name] = button
            nav.addWidget(button)
            self.stack.addWidget(page)
        nav.addStretch()
        body.addLayout(nav)
        body.addWidget(self.stack, 1)
        main.addLayout(body, 1)

    def show_page(self, name):
        page = self.pages.get(name)
        if not page:
            return
        self.stack.setCurrentWidget(page)
        if hasattr(page, "on_show"):
            page.on_show()
