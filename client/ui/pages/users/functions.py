from .api import get_users, create_user, update_user, delete_user


def load(page):
    try:
        result = get_users()
    except Exception as e:
        page.set_data([{"id": "", "username": f"Failed to load users: {e}", "role": ""}])
        return

    if result.get("success"):
        page.set_data(result.get("users", []))


def create(page, data):
    try:
        result = create_user(data)
    except Exception as e:
        print(f"Failed to create user: {e}")
        return

    if result.get("success"):
        page.editing_id = None
        page.clear_form()
        load(page)


def update(page, user_id, data):
    try:
        result = update_user(user_id, data)
    except Exception as e:
        print(f"Failed to update user: {e}")
        return

    if result.get("success"):
        page.editing_id = None
        page.clear_form()
        load(page)


def delete(page, user_id):
    try:
        result = delete_user(user_id)
    except Exception as e:
        print(f"Failed to delete user: {e}")
        return

    if result.get("success"):
        load(page)
