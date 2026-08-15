from .session import session
from ..config import SERVER_URL


def login(username, password):
    response = session.post(
        f"{SERVER_URL}/auth/login",
        json={
            "username": username,
            "password": password,
        },
        timeout=5,
    )

    response.raise_for_status()
    return response.json()


def register(username, password):
    response = session.post(
        f"{SERVER_URL}/auth/register",
        json={
            "username": username,
            "password": password,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()