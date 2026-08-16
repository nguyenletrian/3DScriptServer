from .api import get_apps, create_app, update_app, delete_app


def load(page):
    try:
        result = get_apps()
    except Exception as e:
        page.set_data([{"id": "", "name": f"Failed to load apps: {e}", "description": ""}])
        return

    if result.get("success"):
        page.set_data(result.get("apps", []))


def create(page, data):
    try:
        result = create_app(data)
    except Exception as e:
        print(f"Failed to create app: {e}")
        return

    if result.get("success"):
        page.editing_id = None
        page.clear_form()
        load(page)


def update(page, app_id, data):
    try:
        result = update_app(app_id, data)
    except Exception as e:
        print(f"Failed to update app: {e}")
        return

    if result.get("success"):
        page.editing_id = None
        page.clear_form()
        load(page)


def delete(page, app_id):
    try:
        result = delete_app(app_id)
    except Exception as e:
        print(f"Failed to delete app: {e}")
        return

    if result.get("success"):
        load(page)
