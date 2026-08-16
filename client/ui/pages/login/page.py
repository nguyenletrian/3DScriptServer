from PySide6.QtCore import Signal

from ...builders.page_builder import PageBuilder


PAGE_CONFIG = {
    "title": "Login",
    "form": {
        "popup": False,
        "maximum_width": 300,
        "fields": {
            "username": {
                "type": "text",
                "label": "Username",
                "placeholder": "Enter username",
                "required": True,
            },
            "password": {
                "type": "password",
                "label": "Password",
                "placeholder": "Enter password",
                "required": True,
            },
        },
        "submit_text": "Login",
    },
    "data": {
        "submit": "submit",
    },
}


class LoginPage(PageBuilder):

    login_success = Signal()

    def __init__(self):
        super().__init__(PAGE_CONFIG)
        self.username_edit = self.form.widgets["username"]
        self.password_edit = self.form.widgets["password"]
