from core.security import hash_password
from core.validation import validate_username, validate_password
from .repository import user_repository


def create_user(username, password, role="user"):
    result = validate_username(username)
    if not result["success"]: return result
    result = validate_password(password)
    if not result["success"]: return result
    if user_repository.find_one(username=username): return {"success": False, "message": "Username already exists.", "user": None}
    user = user_repository.insert({"username": username, "password": hash_password(password), "role": role})
    return {"success": True, "message": "User created successfully.", "user": user}


def get_user_by_id(user_id): return user_repository.get(user_id)
def get_all_users(): return user_repository.get_all()


def delete_user(user_id):
    if user_repository.get(user_id) is None: return {"success": False, "message": "User not found."}
    user_repository.delete(user_id)
    return {"success": True, "message": "User deleted."}


def update_user(user_id, username, role, password=None):
    user = user_repository.get(user_id)
    if user is None: return {"success": False, "message": "User not found."}
    result = validate_username(username)
    if not result["success"]: return result
    existing = user_repository.find_one(username=username)
    if existing is not None and existing["id"] != user_id: return {"success": False, "message": "Username already exists."}
    data = {"username": username, "role": role}
    if password:
        result = validate_password(password)
        if not result["success"]: return result
        data["password"] = hash_password(password)
    return {"success": True, "message": "User updated.", "user": user_repository.update(user_id, data)}
