from ....api.users import get_users as _get_users
from ....config import SERVER_URL
from ....session import get_http_session


def get_users():
    return _get_users()


def create_user(data):
    response = get_http_session().post(f"{SERVER_URL}/users", json=data, timeout=5)
    response.raise_for_status()
    return response.json()


def update_user(user_id, data):
    response = get_http_session().put(f"{SERVER_URL}/users/{user_id}", json=data, timeout=5)
    response.raise_for_status()
    return response.json()


def delete_user(user_id):
    response = get_http_session().delete(f"{SERVER_URL}/users/{user_id}", timeout=5)
    response.raise_for_status()
    return response.json()
