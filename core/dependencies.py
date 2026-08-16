from fastapi import Request, HTTPException
from core.repository import BaseRepository


def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None: return None
    return {"id": user_id, "username": request.session.get("username"), "role": request.session.get("role")}


def require_login(request: Request):
    user = get_current_user(request)
    if user is None: raise HTTPException(status_code=401, detail="Login required.")
    return user


def require_admin(request: Request):
    user = require_login(request)
    if user["role"] != "admin": raise HTTPException(status_code=403, detail="Admin access required.")
    return user


def require_instance_access(user, instance_id, write=False):
    if not instance_id: raise HTTPException(status_code=400, detail="application_instance_id is required.")
    if user.get("role") == "admin": return True
    permissions = BaseRepository("application_instance_permissions").get_all()
    permission = next((p for p in permissions if p.get("application_instance_id") == instance_id and p.get("user_id") == user["id"] and p.get("status", "active") == "active"), None)
    if not permission: raise HTTPException(status_code=403, detail="You do not have access to this application instance.")
    if write and not ("*" in permission.get("permissions", []) or any(p.endswith(".write") or p in {"manage", "admin"} for p in permission.get("permissions", []))):
        raise HTTPException(status_code=403, detail="Write access required.")
    return True


def redirect_if_login(request: Request): return get_current_user(request)
