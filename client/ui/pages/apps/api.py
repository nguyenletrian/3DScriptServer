from ....config import SERVER_URL
from ....session import get_http_session


def get_apps():
    response = get_http_session().get(f"{SERVER_URL}/apps", timeout=5)
    response.raise_for_status()
    return response.json()


def create_app(data):
    response = get_http_session().post(f"{SERVER_URL}/apps", json={"data": data}, timeout=5)
    response.raise_for_status()
    return response.json()


def update_app(app_id, data):
    response = get_http_session().put(f"{SERVER_URL}/apps/{app_id}", json={"data": data}, timeout=5)
    response.raise_for_status()
    return response.json()


def delete_app(app_id):
    response = get_http_session().delete(f"{SERVER_URL}/apps/{app_id}", timeout=5)
    response.raise_for_status()
    return response.json()
