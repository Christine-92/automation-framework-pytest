from typing import Dict, Optional, Any
import requests

class BaseClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        # Normalize base_url without trailing slash
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers: Dict[str, str] = {}
        if self.token:
            self.headers['Authorization'] = f"Bearer {self.token}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        return requests.get(url, headers=merged_headers, params=params)

    def post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,   # form-data body (application/x-www-form-urlencoded)
        json: Optional[Any] = None,                # JSON body (application/json)
        headers: Optional[Dict[str, str]] = None,
    ):
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        return requests.post(url, headers=merged_headers, data=params, json=json)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        return requests.delete(url, headers=merged_headers, params=params)
