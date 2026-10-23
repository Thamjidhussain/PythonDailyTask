import requests

from unittest.mock import patch, Mock

from api_monitor import (
    check_url,
    load_urls
)


# ---------------------------------------------------------
# Test 1: Successful API Request
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
def test_successful_request(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_get.return_value = mock_response

    result = check_url(
        "https://example.com",
        max_retries=1
    )

    assert result["success"] is True
    assert result["status_code"] == 200
    assert result["error"] is None


# ---------------------------------------------------------
# Test 2: 404 Response
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
def test_404_response(mock_get):

    mock_response = Mock()

    mock_response.status_code = 404

    mock_get.return_value = mock_response

    result = check_url(
        "https://example.com/not-found",
        max_retries=1
    )

    assert result["success"] is False
    assert result["status_code"] == 404
    assert result["error"] == "HTTP 404"


# ---------------------------------------------------------
# Test 3: 500 Response
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
def test_500_response(mock_get):

    mock_response = Mock()

    mock_response.status_code = 500

    mock_get.return_value = mock_response

    result = check_url(
        "https://example.com/server-error",
        max_retries=1
    )

    assert result["success"] is False
    assert result["status_code"] == 500
    assert result["error"] == "HTTP 500"


# ---------------------------------------------------------
# Test 4: Timeout
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
def test_timeout(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout()

    result = check_url(
        "https://example.com",
        max_retries=1
    )

    assert result["success"] is False
    assert result["status_code"] is None
    assert result["error"] == "Request timed out"


# ---------------------------------------------------------
# Test 5: Invalid URL / Connection Error
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
def test_invalid_url(mock_get):

    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Connection failed"
    )

    result = check_url(
        "https://invalid-url.example",
        max_retries=1
    )

    assert result["success"] is False
    assert result["status_code"] is None
    assert "Connection failed" in result["error"]


# ---------------------------------------------------------
# Test 6: Retry Behavior
# ---------------------------------------------------------

@patch("api_monitor.requests.get")
@patch("api_monitor.time.sleep")
def test_retry_behavior(mock_sleep, mock_get):

    mock_response = Mock()

    mock_response.status_code = 500

    mock_get.return_value = mock_response

    result = check_url(
        "https://example.com",
        max_retries=3
    )

    assert result["success"] is False
    assert result["status_code"] == 500

    # The request should have been attempted 3 times.
    assert mock_get.call_count == 3

    # Sleep should have been called between retries.
    assert mock_sleep.call_count == 2


# ---------------------------------------------------------
# Test 7: Load URLs
# ---------------------------------------------------------

def test_load_urls(tmp_path):

    urls_file = tmp_path / "urls.json"

    urls_file.write_text(
        """
        [
            "https://example.com",
            "https://example.org"
        ]
        """,
        encoding="utf-8"
    )

    urls = load_urls(urls_file)

    assert len(urls) == 2
    assert urls[0] == "https://example.com"
    assert urls[1] == "https://example.org"


# ---------------------------------------------------------
# Test 8: Invalid JSON
# ---------------------------------------------------------

def test_invalid_json(tmp_path):

    urls_file = tmp_path / "urls.json"

    urls_file.write_text(
        "invalid json",
        encoding="utf-8"
    )

    urls = load_urls(urls_file)

    assert urls == []