from ..config import SERVER_URL
from ..session import get_http_session


def get_apps():

    response = get_http_session().get(
        f"{SERVER_URL}/apps",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()

def create_app(name):
    response = get_http_session().post(
        f"{SERVER_URL}/apps",
        json={
            "name": name,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()