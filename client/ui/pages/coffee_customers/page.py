PAGE_CONFIG = {
    "name": "coffee_customers", "title": "Customers", "endpoint": "/coffee/customers", "list": {"data_key": "coffee_customers", "columns": [{"name": "id", "label": "ID"}, {"name": "name", "label": "Name"}, {"name": "phone", "label": "Phone"}, {"name": "note", "label": "Note"}], "actions": ["edit", "delete"]},
    "add_button": {"text": "Add Customer"}, "form": {"fields": {"name": {"type": "text", "label": "Name", "required": True}, "phone": {"type": "text", "label": "Phone", "required": True}, "note": {"type": "textarea", "label": "Note"}}, "submit_text": "Create Customer", "edit_submit_text": "Update Customer", "clear_button": True, "close_button": True, "popup_width": 380}
}
