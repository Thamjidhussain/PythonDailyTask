
from api_client import APIClient


def main():
    client = APIClient(
        "https://jsonplaceholder.typicode.com",
        timeout=5,
        max_attempts=3,
        max_pages=3,
    )

    try:
        users = client.fetch_pages("users", per_page=10)
        print(f"Successfully fetched {len(users)} users")

        for user in users[:10]:
            print(f"ID: {user['id']}, Name: {user['name']}")

    except Exception as exc:
        print(f"API request failed: {exc}")


if __name__ == "__main__":
    main()
