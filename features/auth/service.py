from features.users.service import create_user
from features.users.repository import user_repository
from core.security import verify_password


def authenticate_user(username: str, password: str):
    user = user_repository.find_one(username=username)
    return user if user and verify_password(password, user["password"]) else None


def register_user(username: str, password: str):
    result = create_user(username, password)
    return result["user"] if result["success"] else None
