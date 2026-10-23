from unittest.mock import Mock
import requests
import pytest
from api_client import ApiClient, ApiRequestError

def test_api_success():
    session, response = Mock(), Mock()
    response.json.return_value = [{"id": 1}]
    session.get.return_value = response
    client = ApiClient("https://example.test", session=session)
    assert client.get_json("/users") == [{"id": 1}
    ]
    session.get.assert_called_once_with("https://example.test/users", timeout=5.0)

def test_timeout_retries_then_errors():
    session = Mock()
    session.get.side_effect = requests.Timeout("timeout")
    client = ApiClient("https://example.test", retries=1, session=session)
    with pytest.raises(ApiRequestError):
        client.get_json("/users")
    assert session.get.call_count == 2

def test_404_is_not_retried():
    session, response = Mock(), Mock()
    response.status_code = 404
    response.raise_for_status.side_effect = requests.HTTPError("404", response=response)
    session.get.return_value = response
    with pytest.raises(ApiRequestError):
        ApiClient("https://example.test", retries=3, session=session).get_json("/missing")
    assert session.get.call_count == 1

def test_invalid_url_rejected():
    with pytest.raises(ValueError):
        ApiClient("ftp://example.test")
