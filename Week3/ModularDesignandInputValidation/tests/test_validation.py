
import pytest

from parser import parse_json
from validator import validate_employees
from processor import generate_report


def test_parse_valid_json():
    result = parse_json('[{"id": "E101"}]')
    assert result[0]["id"] == "E101"


def test_malformed_json():
    with pytest.raises(ValueError, match="Invalid JSON input"):
        parse_json('{"id": "E101"')


def test_valid_employees():
    employees = [
        {"id": "E101", "name": "Asha", "salary": 45000},
        {"id": "E102", "name": "Rahul", "salary": 35000},
    ]
    assert len(validate_employees(employees)) == 2


def test_missing_name():
    with pytest.raises(ValueError, match="Employee name"):
        validate_employees([
            {"id": "E101", "salary": 45000}
        ])


def test_negative_salary():
    with pytest.raises(ValueError, match="Salary cannot be negative"):
        validate_employees([
            {"id": "E101", "name": "Asha", "salary": -100}
        ])


def test_duplicate_ids():
    with pytest.raises(ValueError, match="Duplicate employee ID"):
        validate_employees([
            {"id": "E101", "name": "Asha", "salary": 45000},
            {"id": "E101", "name": "Rahul", "salary": 35000},
        ])


def test_empty_input():
    assert validate_employees([]) == []


def test_report_generation():
    employees = [
        {"id": "E101", "name": "Asha", "department": "IT", "salary": 45000},
        {"id": "E102", "name": "Rahul", "department": "IT", "salary": 35000},
    ]
    report = generate_report(employees)

    assert report["total_employees"] == 2
    assert report["department_counts"] == {"IT": 2}
    assert report["total_salary"] == 80000
