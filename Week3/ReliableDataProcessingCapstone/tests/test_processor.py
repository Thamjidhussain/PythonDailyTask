import pytest
from processor import process_records

def test_valid_record_normalized():
    valid, rejected = process_records([{"id": 1, "name": " Ada ", "email": "ADA@EXAMPLE.COM"}])
    assert valid == [{"id": 1, "name": "Ada", "email": "ada@example.com"}]
    assert rejected == []

def test_invalid_rows_rejected_batch_continues():
    valid, rejected = process_records([{"id": 1, "name": "A", "email": "a@x.com"},
                                       {"id": 2, "name": "", "email": "bad"}, "oops"])
    assert len(valid) == 1 and len(rejected) == 2

def test_duplicate_id_rejected():
    row = {"id": 1, "name": "A", "email": "a@x.com"}
    valid, rejected = process_records([row, row])
    assert len(valid) == 1 and rejected[0]["reason"] == "duplicate id"

def test_empty_list_boundary():
    assert process_records([]) == ([], [])

def test_non_list_payload_error():
    with pytest.raises(ValueError):
        process_records({"id": 1})
