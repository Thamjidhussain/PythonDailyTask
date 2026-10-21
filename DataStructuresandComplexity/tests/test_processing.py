
import pytest
from processing import process_employees


def test_valid_employees():
    employees = [
        {"id": "E101", "name": "Asha"},
        {"id": "E102", "name": "Rahul"},
    ]
    result = process_employees(employees)

    assert len(result["employees"]) == 2
    assert result["employee_index"]["E101"]["name"] == "Asha"
    assert result["processed_ids"] == ["E101", "E102"]


def test_duplicate_ids():
    employees = [
        {"id": "E101", "name": "Asha"},
        {"id": "E101", "name": "Duplicate"},
    ]
    result = process_employees(employees)

    assert len(result["employees"]) == 1
    assert result["duplicates"] == ["E101"]


def test_empty_input():
    result = process_employees([])

    assert result["employees"] == []
    assert result["employee_index"] == {}
    assert result["processed_ids"] == []


def test_missing_id():
    with pytest.raises(ValueError, match="Employee ID cannot be empty"):
        process_employees([{"name": "Asha"}])


def test_empty_id():
    with pytest.raises(ValueError, match="Employee ID cannot be empty"):
        process_employees([{"id": "", "name": "Asha"}])
