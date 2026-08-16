from .... import session
from ....api.auth import login


def submit(page, data):
    page.set_error("")

    try:
        result = login(data["username"], data["password"])
    except Exception as e:
        page.set_error(f"Connection error: {e}")
        return

    if not result.get("success"):
        page.set_error(result.get("message", "Invalid username or password."))
        return

    session.set_user(result["user"])
    page.login_success.emit()
