import pytest

from employee_app.validators import (
    ValidationError, validate_email, validate_employee_id, validate_salary
)


def test_valid_email():
    assert validate_email("alex@example.com") == "alex@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        validate_email("not-an-email")


def test_valid_employee_id():
    assert validate_employee_id("E-101") == "E-101"


def test_negative_salary():
    with pytest.raises(ValidationError):
        validate_salary(-100)
