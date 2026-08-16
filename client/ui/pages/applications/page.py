PAGE_CONFIG = {
    "name": "applications",
    "title": "Applications",
    "endpoint": "/applications",
    "payload_key": "data",
    "admin_only": ["add", "edit", "delete"],
    "list": {
        "columns": [
            {"name": "id", "label": "ID"},
            {"name": "name", "label": "Name"},
            {"name": "description", "label": "Description"},
        ],
        "actions": ["activate", "edit", "delete"],
    },
}
