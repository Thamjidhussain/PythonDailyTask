
import requests
import pytest
from unittest.mock import Mock

from api_client import APIClient


@pytest.fixture
def session():
    return Mock()


@pytest.fixture
def client(session):
    return APIClient(
        "https://example.test",
        timeout=2,
        max_attempts=3,
        max_pages=2,
        session=session,
    )


def response(status=200, data=None):
    result = Mock()
    result.status_code = status
    result.json.return_value = data
    result.raise_for_status.side_effect = (
        requests.HTTPError(f"HTTP {status}") if status >= 400 else None
    )
    return result


def test_successful_json_response(client, session):
    session.get.return_value = response(200, [{"id": 1}])

    result = client.get_json("https://example.test/items")

    assert result == [{"id": 1}]
    assert session.get.call_count == 1
    assert session.get.call_args.kwargs["timeout"] == 2


def test_timeout_retries_then_succeeds(client, session, monkeypatch):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)
    session.get.side_effect = [
        requests.Timeout(),
        response(200, [{"id": 1}]),
    ]

    result = client.get_json("https://example.test/items")

    assert result == [{"id": 1}]
    assert session.get.call_count == 2


def test_timeout_stops_after_max_attempts(client, session, monkeypatch):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)
    session.get.side_effect = requests.Timeout()

    with pytest.raises(requests.Timeout):
        client.get_json("https://example.test/items")

    assert session.get.call_count == 3


def test_server_error_retries(client, session, monkeypatch):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)
    session.get.side_effect = [
        response(503),
        response(200, [{"id": 1}]),
    ]

    assert client.get_json("https://example.test/items") == [{"id": 1}]
    assert session.get.call_count == 2


def test_not_found_is_not_retried(client, session):
    session.get.return_value = response(404)

    with pytest.raises(requests.HTTPError):
        client.get_json("https://example.test/missing")

    assert session.get.call_count == 1


def test_malformed_json_is_not_retried(client, session):
    result = response(200)
    result.json.side_effect = ValueError("Invalid JSON")
    session.get.return_value = result

    with pytest.raises(ValueError, match="Invalid JSON"):
        client.get_json("https://example.test/items")

    assert session.get.call_count == 1


def test_pagination_stops_at_configured_limit(client, session):
    session.get.side_effect = [
        response(200, [{"id": 1}]),
        response(200, [{"id": 2}]),
    ]

    result = client.fetch_pages("items", per_page=1)

    assert result == [{"id": 1}, {"id": 2}]
    assert session.get.call_count == 2


def test_invalid_page_size(client):
    with pytest.raises(ValueError, match="per_page"):
        client.fetch_pages("items", per_page=0)
