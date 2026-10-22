
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
        requests.HTTPError(f"HTTP {status}")
        if status >= 400
        else None
    )
    return result


# Test 1: Successful API response
def test_successful_json_response(client, session):
    session.get.return_value = response(200, [{"id": 1}])

    result = client.get_json("https://example.test/items")

    assert result == [{"id": 1}]
    assert session.get.call_count == 1
    assert session.get.call_args.kwargs["timeout"] == 2


# Test 2: Timeout retry succeeds
def test_timeout_retries_then_succeeds(client, session, monkeypatch):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)

    session.get.side_effect = [
        requests.Timeout(),
        response(200, [{"id": 1}]),
    ]

    result = client.get_json("https://example.test/items")

    assert result == [{"id": 1}]
    assert session.get.call_count == 2


# Test 3: Timeout stops after maximum attempts
def test_timeout_stops_after_max_attempts(
    client, session, monkeypatch
):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)
    session.get.side_effect = requests.Timeout()

    with pytest.raises(requests.Timeout):
        client.get_json("https://example.test/items")

    assert session.get.call_count == 3


# Test 4: Server error retry
def test_server_error_retries(client, session, monkeypatch):
    monkeypatch.setattr("api_client.time.sleep", lambda _: None)

    session.get.side_effect = [
        response(503),
        response(200, [{"id": 1}]),
    ]

    result = client.get_json("https://example.test/items")

    assert result == [{"id": 1}]
    assert session.get.call_count == 2


# Test 5: HTTP 404 should not retry
def test_not_found_is_not_retried(client, session):
    session.get.return_value = response(404)

    with pytest.raises(requests.HTTPError):
        client.get_json("https://example.test/missing")

    assert session.get.call_count == 1


# Test 6: Invalid JSON
def test_malformed_json_is_not_retried(client, session):
    result = response(200)
    result.json.side_effect = ValueError("Invalid JSON")
    session.get.return_value = result

    with pytest.raises(ValueError, match="Invalid JSON"):
        client.get_json("https://example.test/items")

    assert session.get.call_count == 1


# Test 7: Pagination limit
def test_pagination_stops_at_configured_limit(client, session):
    session.get.side_effect = [
        response(200, [{"id": 1}]),
        response(200, [{"id": 2}]),
    ]

    result = client.fetch_pages("items", per_page=1)

    assert result == [{"id": 1}, {"id": 2}]
    assert session.get.call_count == 2


# Test 8: Original invalid page size
def test_invalid_page_size(client):
    with pytest.raises(ValueError, match="per_page"):
        client.fetch_pages("items", per_page=0)


# Test 9: Reusable sample users fixture
def test_sample_users_fixture(sample_users):
    assert len(sample_users) == 2
    assert sample_users[0]["name"] == "Leanne Graham"
    assert sample_users[1]["name"] == "Ervin Howell"


# Test 10: Empty users fixture
def test_empty_users_fixture(empty_users):
    assert empty_users == []


# Test 11: Valid page sizes fixture
def test_valid_page_sizes_fixture(valid_page_sizes):
    assert valid_page_sizes == [1, 10, 100]


# Test 12: Invalid page sizes fixture
def test_invalid_page_sizes_fixture(invalid_page_sizes):
    assert invalid_page_sizes == [0, -1, 101]


# Tests 13-15: Parametrized valid page sizes
@pytest.mark.parametrize("page_size", [1, 10, 100])
def test_valid_page_size(page_size, client, session):
    """Verify valid page sizes using the actual API client."""
    session.get.return_value = response(200, [])

    result = client.fetch_pages("items", per_page=page_size)

    assert result == []
    assert session.get.call_count == 1


# Tests 16-18: Parametrized invalid page sizes

@pytest.mark.parametrize("page_size", [0, -1])
def test_invalid_page_size_parametrized(page_size, client, session):
    """Verify page sizes below the minimum are rejected."""
    with pytest.raises(ValueError, match="per_page"):
        client.fetch_pages("items", per_page=page_size)

    assert session.get.call_count == 0

