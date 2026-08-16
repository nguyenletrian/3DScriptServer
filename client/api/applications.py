from ..config import SERVER_URL
from ..session import get_http_session
from .application_instances import activate_application as _activate_application


def get_applications():
    response = get_http_session().get(f"{SERVER_URL}/applications", timeout=5)
    response.raise_for_status()
    return response.json()


def create_application(data):
    response = get_http_session().post(f"{SERVER_URL}/applications", json={"data": data}, timeout=5)
    response.raise_for_status()
    return response.json()


def update_application(application_id, data):
    response = get_http_session().put(f"{SERVER_URL}/applications/{application_id}", json={"data": data}, timeout=5)
    response.raise_for_status()
    return response.json()


def delete_application(application_id):
    response = get_http_session().delete(f"{SERVER_URL}/applications/{application_id}", timeout=5)
    response.raise_for_status()
    return response.json()


def activate_application(application_id):
    return _activate_application(application_id)
