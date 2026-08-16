PAGE_CONFIG = {
    "name": "coffee_categories", "title": "Categories", "endpoint": "/coffee/categories", "list": {"data_key": "coffee_categories", "columns": [{"name": "id", "label": "ID"}, {"name": "name", "label": "Name"}, {"name": "status", "label": "Status"}], "actions": ["edit", "delete"]},
    "add_button": {"text": "Add Category"}, "form": {"fields": {"name": {"type": "text", "label": "Name", "required": True}, "status": {"type": "select", "label": "Status", "options": ["active", "inactive"], "required": True}}, "submit_text": "Create Category", "edit_submit_text": "Update Category", "clear_button": True, "close_button": True, "popup_width": 360}
}
