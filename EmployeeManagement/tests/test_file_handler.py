import pytest

import employee_app.file_handler as fh
from employee_app.validators import DataFileError


def test_json_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    data = [{"employee_id": "E101", "name": "Rahul"}]
    fh.write_json("sample.json", data)
    assert fh.read_json("sample.json") == data


def test_missing_json_returns_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    assert fh.read_json("missing.json") == []


def test_invalid_json_raises_error(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    (tmp_path / "broken.json").write_text("{bad json", encoding="utf-8")
    with pytest.raises(DataFileError):
        fh.read_json("broken.json")
