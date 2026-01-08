# ingestion/api_client.py

import requests
from typing import List, Dict


class APIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, endpoint: str) -> List[Dict]:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

