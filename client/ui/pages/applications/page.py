PAGE_CONFIG = {
    "name": "applications", "title": "Applications", "endpoint": "/applications", "payload_key": "data",
    "admin_only": ["add", "edit", "delete"],
    "data": {"activate": "activate"},
    "add_button": {"text": "Add Application"},
    "form": {
        "fields": {"name": {"type": "text", "label": "Name", "required": True}, "description": {"type": "textarea", "label": "Description"}},
        "submit_text": "Create Application", "edit_submit_text": "Update Application", "clear_button": True, "close_button": True, "popup_width": 360, "maximum_width": 300,
    },
    "list": {
        "columns": [{"name": "id", "label": "ID"}, {"name": "name", "label": "Name"}, {"name": "description", "label": "Description"}],
        "actions": ["activate", "edit", "delete"],
    },
}
