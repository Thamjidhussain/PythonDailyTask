
import json
import pytest

import library_app.file_handler as fh
from library_app.validators import DataFileError


def test_write_and_read_json(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)

    data = [{"book_id": "B101", "title": "Python"}]

    fh.write_json("books.json", data)

    assert fh.read_json("books.json") == data


def test_missing_file_returns_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)

    assert fh.read_json("books.json") == []


def test_invalid_json_raises_error(tmp_path, monkeypatch):
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    (tmp_path / "books.json").write_text(
        "{invalid json", encoding="utf-8"
    )

    with pytest.raises(DataFileError):
        fh.read_json("books.json")
