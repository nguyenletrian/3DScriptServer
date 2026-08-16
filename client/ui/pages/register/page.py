from PySide6.QtCore import Signal

from ...builders.page_builder import PageBuilder


PAGE_CONFIG = {
    "name": "register",
    "title": "Register",
    "form": {
        "popup": False,
        "maximum_width": 360,
        "fields": {
            "username": {"type": "text", "label": "Username", "placeholder": "Enter username", "required": True},
            "password": {"type": "password", "label": "Password", "placeholder": "Enter password", "required": True},
            "confirm_password": {"type": "password", "label": "Confirm Password", "placeholder": "Confirm password", "required": True},
        },
        "submit_text": "Register",
    },
    "data": {"submit": "submit"},
}


class RegisterPage(PageBuilder):
    register_success = Signal()

    def __init__(self):
        super().__init__(PAGE_CONFIG)
        self.username_edit = self.form.widgets["username"]
        self.password_edit = self.form.widgets["password"]
        self.confirm_password_edit = self.form.widgets["confirm_password"]
