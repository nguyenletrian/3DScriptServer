from ....api.users import get_users


def load(page):
    try:
        result = get_users()
    except Exception as e:
        page.set_data([
            {
                "id": "",
                "username": f"Failed to load users: {e}",
                "role": "",
            }
        ])
        return

    if result.get("success"):
        page.set_data(result.get("users", []))
