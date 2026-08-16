from ....api.auth import register


def submit(page, data):
    if data["password"] != data["confirm_password"]:
        page.set_error("Passwords do not match.")
        return
    try:
        result = register(data["username"].strip(), data["password"])
    except Exception as e:
        page.set_error(f"Connection error: {e}")
        return
    if not result.get("success"):
        page.set_error(result.get("message", "Registration failed."))
        return
    page.register_success.emit()
