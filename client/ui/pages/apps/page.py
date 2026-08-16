PAGE_CONFIG = {
    "name": "apps",
    "title": "Apps",
    "add_button": {"text": "Add App"},
    "form": {
        "fields": {
            "name": {"type": "text", "label": "Name", "required": True},
            "description": {"type": "textarea", "label": "Description"},
        },
        "submit_text": "Create App", "edit_submit_text": "Update App",
        "clear_button": True, "close_button": True, "popup_width": 360, "maximum_width": 300,
    },
    "list": {
        "columns": [{"name": "id", "label": "ID"}, {"name": "name", "label": "Name"}, {"name": "description", "label": "Description"}],
        "actions": ["edit", "delete"],
    },
}
