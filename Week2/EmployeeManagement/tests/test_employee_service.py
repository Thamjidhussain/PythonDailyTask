import pytest

from employee_app.employee_service import EmployeeService
from employee_app.validators import DuplicateEmployeeError, EmployeeNotFoundError, ValidationError


@pytest.fixture
def service(tmp_path, monkeypatch):
    import employee_app.file_handler as fh
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    return EmployeeService()


def test_add_employee(service):
    employee = service.add_employee(
        "E101", "Rahul Kumar", "rahul@example.com", "IT", 45000
    )
    assert employee.employee_id == "E101"
    assert employee.salary == 45000


def test_duplicate_employee_rejected(service):
    service.add_employee("E101", "Rahul", "rahul@example.com", "IT", 45000)
    with pytest.raises(DuplicateEmployeeError):
        service.add_employee("E101", "Ravi", "ravi@example.com", "HR", 30000)


def test_search_employee(service):
    service.add_employee("E101", "Rahul Kumar", "rahul@example.com", "IT", 45000)
    assert len(service.search_employees("rahul")) == 1


def test_invalid_salary_rejected(service):
    with pytest.raises(ValidationError):
        service.add_employee("E101", "Rahul", "rahul@example.com", "IT", -1)


def test_missing_employee(service):
    with pytest.raises(EmployeeNotFoundError):
        service.get_employee("E999")
