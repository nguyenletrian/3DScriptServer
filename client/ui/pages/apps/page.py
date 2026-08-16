from ...builders.page_builder import PageBuilder


PAGE_CONFIG = {
    "title": "Apps",
    "add_button": {"text": "Add App"},
    "data": {
        "loader": "load",
        "creator": "create",
        "updater": "update",
        "deleter": "delete",
    },
    "form": {
        "fields": {
            "name": {"type": "text", "label": "Name", "required": True},
            "description": {"type": "textarea", "label": "Description"},
        },
        "submit_text": "Create App",
        "edit_submit_text": "Update App",
    },
    "list": {
        "columns": [
            {"name": "id", "label": "ID"},
            {"name": "name", "label": "Name"},
            {"name": "description", "label": "Description"},
        ],
        "actions": ["edit", "delete"],
    },
}


class AppsPage(PageBuilder):

    def __init__(self):
        super().__init__(PAGE_CONFIG)
