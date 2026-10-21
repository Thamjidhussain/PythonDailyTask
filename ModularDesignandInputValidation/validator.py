
def validate_employee(employee):
    if not isinstance(employee, dict):
        raise ValueError("Employee must be a JSON object")

    employee_id = employee.get("id")
    name = employee.get("name")
    salary = employee.get("salary")

    if not isinstance(employee_id, str) or not employee_id.strip():
        raise ValueError("Employee ID must be a non-empty string")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Employee name must be a non-empty string")

    # Reject booleans, which Python otherwise treats as integers.
    if isinstance(salary, bool) or not isinstance(salary, (int, float)):
        raise ValueError("Salary must be a number")

    if salary < 0:
        raise ValueError("Salary cannot be negative")

    return employee


def validate_employees(data):
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON array of employees")

    seen_ids = set()

    for employee in data:
        validate_employee(employee)
        employee_id = employee["id"]

        if employee_id in seen_ids:
            raise ValueError(f"Duplicate employee ID: {employee_id}")

        seen_ids.add(employee_id)

    return data
