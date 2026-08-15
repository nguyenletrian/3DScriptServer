from ..session import get_http_session
from ..config import SERVER_URL


def get_users():
    response = get_http_session().get(
        f"{SERVER_URL}/users",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()