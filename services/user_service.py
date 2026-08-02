import json
from utils.password import (hash_password,verify_password)
from utils.validation import (validate_password,validate_username)


def create_user(username,password,role="user"):
    username_check = validate_username(username)
    if not username_check["success"]:
        return username_check

    password_check = validate_password(password)
    if not password_check["success"]:
        return password_check

    if find_user(username):
        return {
            "success": False,
            "message": "Username already exists.",
            "user": None
        }    
    users = load_users()
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": hash_password(password),
        "role":role
    }
    users.append(new_user)
    save_users(users)
    return {
        "success": True,
        "message": "User created successfully.",
        "user": new_user
    }

def authenticate_user(username,password):
    username_check = validate_username(username)
    if not username_check["success"]:
        return username_check

    user = find_user(username)
    if user is None:
        return {
            "success": False,
            "message": "Username not found.",
            "user":None,
        }
    if not verify_password(
        password,
        user["password"]
    ):
        return {
            "success": False,
            "message": "Wrong password.",
            "user": None
        }
    return {
        "success": True,
        "message": "Login success.",
        "user": user
    }

def get_user_by_id(user_id):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def load_users():
    with open(
        "database/users.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)

def get_all_users():
    return load_users()

def save_users(users):
    with open(
        "database/users.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            users,
            file,
            indent=4,
            ensure_ascii=False
        )


def find_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

def delete_user(user_id):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            save_users(users)
            return {
                "success": True,
                "message": "User deleted."
            }
    return {
        "success": False,
        "message": "User not found."
    }

def update_user(user_id,username,role):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            user["username"] = username
            user["role"] = role
            break
    save_users(users)