from ..session import get_http_session, set_user
from ..config import SERVER_URL


def login(username, password):
    response = get_http_session().post(
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
    response = get_http_session().post(
        f"{SERVER_URL}/auth/register",
        json={
            "username": username,
            "password": password,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()

def logout():
    response = get_http_session().post(
        f"{SERVER_URL}/auth/logout",
        timeout=5,
    )
    response.raise_for_status()
    return response.json()