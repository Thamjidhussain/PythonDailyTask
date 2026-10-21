
import time

import requests


RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


class APIClient:
    def __init__(
        self,
        base_url,
        timeout=5,
        max_attempts=3,
        max_pages=5,
        session=None,
    ):
        if timeout <= 0:
            raise ValueError("Timeout must be positive")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if max_pages < 1:
            raise ValueError("max_pages must be at least 1")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.max_pages = max_pages
        self.session = session or requests.Session()

    def get_json(self, url, params=None):
        """GET JSON, retrying only selected transient failures."""
        for attempt in range(self.max_attempts):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                )

                if response.status_code in RETRYABLE_STATUS_CODES:
                    if attempt + 1 < self.max_attempts:
                        time.sleep(0.2 * (attempt + 1))
                        continue

                response.raise_for_status()
                return response.json()

            except (requests.Timeout, requests.ConnectionError):
                if attempt + 1 >= self.max_attempts:
                    raise
                time.sleep(0.2 * (attempt + 1))

            except requests.HTTPError:
                # Retry only the explicitly selected transient statuses.
                if (
                    attempt + 1 >= self.max_attempts
                    or response.status_code not in RETRYABLE_STATUS_CODES
                ):
                    raise

                time.sleep(0.2 * (attempt + 1))

        raise RuntimeError("API request failed")

    def fetch_pages(self, path, per_page=10):
        """Fetch a bounded number of numbered JSON pages."""
        if per_page < 1:
            raise ValueError("per_page must be at least 1")

        url = f"{self.base_url}/{path.lstrip('/')}"
        records = []

        for page in range(1, self.max_pages + 1):
            data = self.get_json(
                url,
                params={"_page": page, "_limit": per_page},
            )

            if not isinstance(data, list):
                raise ValueError("Expected a JSON array from the API")

            if not data:
                break

            records.extend(data)

            # A short page indicates there may be no more records.
            if len(data) < per_page:
                break

        return records
