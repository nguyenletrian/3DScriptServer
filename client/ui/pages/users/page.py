PAGE_CONFIG = {
    "name": "users",
    "title": "Users",
    "endpoint": "/users",
    "add_button": {"text": "Add User"},
    "form": {
        "popup": True,
        "fields": {
            "username": {"type": "text", "label": "Username", "required": True},
            "password": {"type": "password", "label": "Password"},
            "role": {"type": "select", "label": "Role", "options": ["user", "admin"], "required": True},
        },
        "submit_text": "Create User", "edit_submit_text": "Update User",
        "clear_button": True, "close_button": True, "popup_width": 360,
    },
    "list": {
        "columns": [{"name": "id", "label": "ID"}, {"name": "username", "label": "Username"}, {"name": "role", "label": "Role"}],
        "actions": ["edit", "delete"],
    },
}
