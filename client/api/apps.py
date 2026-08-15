from ..config import SERVER_URL
from ..session import get_http_session


def get_apps():

    response = get_http_session().get(
        f"{SERVER_URL}/apps",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()