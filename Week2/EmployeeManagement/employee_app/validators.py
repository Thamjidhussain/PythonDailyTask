import re


class EmployeeAppError(Exception):
    """Base exception for application errors."""


class EmployeeNotFoundError(EmployeeAppError):
    """Raised when an employee cannot be found."""


class DuplicateEmployeeError(EmployeeAppError):
    """Raised when an employee ID already exists."""


class ValidationError(EmployeeAppError):
    """Raised when employee data is invalid."""


class DataFileError(EmployeeAppError):
    """Raised when a data file cannot be read or written."""


def validate_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_employee_id(value):
    value = validate_text(value, "Employee ID")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValidationError(
            "Employee ID may contain letters, numbers, underscores, or hyphens."
        )
    return value


def validate_email(value):
    value = validate_text(value, "Email")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise ValidationError("Enter a valid email address.")
    return value


def validate_salary(value):
    if isinstance(value, bool):
        raise ValidationError("Salary must be a number greater than or equal to zero.")
    try:
        salary = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Salary must be a number.") from exc
    if salary < 0:
        raise ValidationError("Salary cannot be negative.")
    return salary


def validate_employee_data(employee_id, name, email, department, salary):
    return {
        "employee_id": validate_employee_id(employee_id),
        "name": validate_text(name, "Name"),
        "email": validate_email(email),
        "department": validate_text(department, "Department"),
        "salary": validate_salary(salary),
    }
