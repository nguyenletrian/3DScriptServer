PAGE_CONFIG = {
    "name": "users",
    "title": "Users",
    "add_button": {"text": "Add User"},
    "data": {"loader": "load", "creator": "create", "updater": "update", "deleter": "delete"},
    "form": {
        "popup": True,
        "fields": {
            "username": {"type": "text", "label": "Username", "required": True},
            "password": {"type": "password", "label": "Password"},
            "role": {"type": "text", "label": "Role", "required": True},
        },
        "submit_text": "Create User", "edit_submit_text": "Update User",
        "clear_button": True, "close_button": True, "popup_width": 360, "maximum_width": 300,
    },
    "list": {
        "columns": [{"name": "id", "label": "ID"}, {"name": "username", "label": "Username"}, {"name": "role", "label": "Role"}],
        "actions": ["edit", "delete"],
    },
}
