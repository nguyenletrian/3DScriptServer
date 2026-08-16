import requests

from ..config import SERVER_URL
from ..session import get_http_session


class RestAPI:
    def __init__(self, endpoint, payload_key=None, instance_id=None):
        self.url = f"{SERVER_URL}/{endpoint.strip('/')}"
        self.payload_key = payload_key
        self.instance_id = instance_id

    def _request(self, method, path="", data=None):
        payload = {self.payload_key: data} if self.payload_key and data is not None else data
        params = {"application_instance_id": self.instance_id} if self.instance_id else None
        response = get_http_session().request(method, f"{self.url}{path}", params=params, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()

    def get(self): return self._request("GET")
    def create(self, data): return self._request("POST", data=data)
    def update(self, item_id, data): return self._request("PUT", f"/{item_id}", data)
    def delete(self, item_id): return self._request("DELETE", f"/{item_id}")
