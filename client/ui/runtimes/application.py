from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget

from ..builders.page_builder import build_page


class ApplicationRuntime(QWidget):
    PAGE_NAMES = []
    TITLE = "Application"

    def __init__(self, instance=None, parent=None):
        super().__init__(parent)
        self.instance = instance or {}
        self.pages = {name: build_page(name, self.instance) for name in self.PAGE_NAMES}
        self.stack = QStackedWidget()
        self.nav_widget = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        main = QVBoxLayout(self)
        header = QHBoxLayout()
        title = QLabel(self.instance.get("name") or self.TITLE)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title); header.addStretch()
        back = QPushButton("Applications")
        back.clicked.connect(lambda: self.window().show_page("applications"))
        header.addWidget(back)
        main.addLayout(header)

        body = QHBoxLayout()
        toggle = QPushButton("☰")
        toggle.setFixedWidth(36); toggle.setToolTip("Show / Hide navigation")
        toggle.clicked.connect(self.toggle_navigation)
        nav_header = QHBoxLayout(); nav_header.addWidget(toggle); nav_header.addStretch()
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        container = QVBoxLayout(); container.addLayout(nav_header); container.addWidget(self.nav_widget)
        nav_panel = QWidget(); nav_panel.setLayout(container); nav_panel.setMinimumWidth(160)
        body.addWidget(nav_panel)
        for name, page in self.pages.items():
            button = QPushButton(page.config.get("title", name)); button.clicked.connect(lambda checked=False, n=name: self.show_page(n)); self.buttons[name] = button; self.nav_layout.addWidget(button); self.stack.addWidget(page)
        self.nav_layout.addStretch(); body.addWidget(self.stack, 1); main.addLayout(body, 1)
        self.nav_panel = nav_panel

    def toggle_navigation(self):
        self.nav_panel.setVisible(not self.nav_panel.isVisible())

    def show_page(self, name):
        page = self.pages.get(name)
        if not page: return
        self.stack.setCurrentWidget(page)
        if hasattr(page, "on_show"): page.on_show()
