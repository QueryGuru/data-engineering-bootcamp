# ingestion/main.py

from ingestion.config import BASE_URL, ENDPOINTS
from ingestion.api_client import APIClient


def run():
    client = APIClient(base_url=BASE_URL)

    tickets = client.get(ENDPOINTS["tickets"])
    users = client.get(ENDPOINTS["users"])

    print(f"Fetched {len(tickets)} tickets")
    print(f"Fetched {len(users)} users")


if __name__ == "__main__":
    run()

