from core.audit import record_audit
from core.security import hash_password
from core.validation import validate_username, validate_password
from .repository import user_repository


def _safe(user):
    if not user: return user
    return {key: value for key, value in user.items() if key != "password"}


def create_user(username, password, role="user", actor_id=None):
    result = validate_username(username)
    if not result["success"]: return result
    result = validate_password(password)
    if not result["success"]: return result
    if user_repository.find_one(username=username): return {"success": False, "message": "Username already exists.", "user": None}
    user = user_repository.insert({"username": username, "password": hash_password(password), "role": role})
    safe_user = _safe(user)
    record_audit(actor_id, "create", "user", user["id"], after=safe_user, metadata={"source": "web"})
    return {"success": True, "message": "User created successfully.", "user": safe_user}


def get_user_by_id(user_id): return _safe(user_repository.get(user_id))
def get_all_users(): return [_safe(user) for user in user_repository.get_all()]


def delete_user(user_id, actor_id=None):
    user = user_repository.get(user_id)
    if user is None: return {"success": False, "message": "User not found."}
    user = _safe(user)
    user_repository.delete(user_id)
    record_audit(actor_id, "delete", "user", user_id, before=user, metadata={"source": "web"})
    return {"success": True, "message": "User deleted."}


def update_user(user_id, username, role, password=None, actor_id=None):
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
    before = _safe(user)
    updated = user_repository.update(user_id, data)
    safe_user = _safe(updated)
    record_audit(actor_id, "update", "user", user_id, before=before, after=safe_user, metadata={"source": "web"})
    return {"success": True, "message": "User updated.", "user": safe_user}
