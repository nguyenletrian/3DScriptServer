def validate_username(username: str):
    if not username:
        return {
            "success": False,
            "message": "Username is required."
        }

    if len(username) < 3:
        return {
            "success": False,
            "message": "Username must be at least 3 characters."
        }

    return {
        "success": True
    }


def validate_password(password: str):
    if not password:
        return {
            "success": False,
            "message": "Password is required."
        }

    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters."
        }

    return {
        "success": True
    }