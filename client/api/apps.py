import requests

from ..config import SERVER_URL


def get_apps():

    response = requests.get(
        f"{SERVER_URL}/apps",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()