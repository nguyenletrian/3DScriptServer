from core.security import hash_password
from core.validation import validate_username, validate_password
from .repository import user_repository


def create_user(username, password, role="user"):
    username_check = validate_username(username)
    if not username_check["success"]:
        return username_check

    password_check = validate_password(password)
    if not password_check["success"]:
        return password_check

    if user_repository.find_by_username(username):
        return {
            "success": False,
            "message": "Username already exists.",
            "user": None,
        }

    user = user_repository.insert({
        "username": username,
        "password": hash_password(password),
        "role": role,
    })

    return {
        "success": True,
        "message": "User created successfully.",
        "user": user,
    }


def get_user_by_id(user_id):
    return user_repository.get(user_id)


def get_all_users():
    return user_repository.get_all()


def delete_user(user_id):
    user = user_repository.get(user_id)
    if user is None:
        return {
            "success": False,
            "message": "User not found.",
        }

    user_repository.delete(user_id)
    return {
        "success": True,
        "message": "User deleted.",
    }


def update_user(user_id, username, role, password=None):
    user = user_repository.get(user_id)
    if user is None:
        return {
            "success": False,
            "message": "User not found.",
        }

    username_check = validate_username(username)
    if not username_check["success"]:
        return username_check

    existing_user = user_repository.find_by_username(username)
    if existing_user is not None and existing_user["id"] != user_id:
        return {
            "success": False,
            "message": "Username already exists.",
        }

    data = {
        "username": username,
        "role": role,
    }

    if password:
        password_check = validate_password(password)
        if not password_check["success"]:
            return password_check
        data["password"] = hash_password(password)

    updated_user = user_repository.update(user_id, data)

    return {
        "success": True,
        "message": "User updated.",
        "user": updated_user,
    }
