import logging
import time
import requests

log = logging.getLogger(__name__)

class ApiClientError(RuntimeError):
    pass

class ApiRequestError(ApiClientError):
    pass

class ApiClient:
    def __init__(self, base_url, timeout=5.0, retries=2, session=None):
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("base_url must use HTTP or HTTPS")
        if timeout <= 0 or retries < 0:
            raise ValueError("timeout must be positive and retries non-negative")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.session = session or requests.Session()

    def get_json(self, endpoint=""):
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        for attempt in range(self.retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                try:
                    return response.json()
                except ValueError as exc:
                    raise ApiRequestError("API returned invalid JSON") from exc
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as exc:
                status = getattr(getattr(exc, "response", None), "status_code", None)
                retryable = isinstance(exc, (requests.Timeout, requests.ConnectionError)) or (
                    status is not None and status >= 500)
                if not retryable or attempt == self.retries:
                    log.error("API request failed: %s", type(exc).__name__)
                    raise ApiRequestError(f"API request failed: {type(exc).__name__}") from exc
                log.warning("Retrying API request (%s/%s)", attempt + 1, self.retries)
                time.sleep(min(0.1 * (attempt + 1), 0.5))
