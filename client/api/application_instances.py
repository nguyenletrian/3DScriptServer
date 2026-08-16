from ..config import SERVER_URL
from ..session import get_http_session


def get_application_instances():
    response = get_http_session().get(f"{SERVER_URL}/application-instances", timeout=5)
    response.raise_for_status()
    return response.json()


def activate_application(application_id, data=None):
    payload = dict(data or {})
    payload["application_id"] = application_id
    response = get_http_session().post(f"{SERVER_URL}/application-instances/activate", json=payload, timeout=5)
    response.raise_for_status()
    return response.json()
