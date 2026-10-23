import json
from unittest.mock import patch
from main import run
from api_client import ApiRequestError

def test_workflow_writes_report(tmp_path):
    path = tmp_path / "report.json"
    data = [{"id": 1, "name": "Ada", "email": "ada@example.com"},
            {"id": 2, "name": "", "email": "bad"}]
    with patch("main.ApiClient.get_json", return_value=data):
        assert run("https://example.test", "/users", str(path), 2, 0) == 0
    report = json.loads(path.read_text())
    assert report["summary"] == {"received": 2, "processed": 1, "rejected": 1}

def test_api_failure_does_not_write_report(tmp_path):
    path = tmp_path / "report.json"
    with patch("main.ApiClient.get_json", side_effect=ApiRequestError("offline")):
        assert run("https://example.test", "/users", str(path), 2, 0) == 1
    assert not path.exists()
