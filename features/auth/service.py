from features.users.repository import user_repository
from core.security import verify_password,hash_password


def authenticate_user(
    username: str,
    password: str
):
    user = user_repository.find_one(
        username=username
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user["password"]
    ):
        return None

    return user


def register_user(username: str,password: str):
    existing_user = user_repository.find_one(username=username)
    if existing_user is not None:
        return None
    users = user_repository.get_all()
    if users:
        user_id = max(
            user["id"]
            for user in users
        ) + 1
    else:
        user_id = 1
        
    hashed_password = hash_password(
        password
    )
    user = {
        "id": user_id,
        "username": username,
        "password": hashed_password,
        "role": "user"
    }
    return user_repository.insert(user)