from .session import session
from ..config import SERVER_URL


def get_users():
    response = session.get(
        f"{SERVER_URL}/users",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()