from employee_app.models import Employee
from employee_app.file_handler import read_json, write_json, read_csv
from employee_app.validators import (
    DataFileError,
    DuplicateEmployeeError,
    EmployeeNotFoundError,
    ValidationError,
    validate_employee_data,
)


class EmployeeService:
    JSON_FILE = "employees.json"
    CSV_FILE = "employees.csv"

    def __init__(self):
        self.employees = []
        for row in read_json(self.JSON_FILE):
            try:
                self.employees.append(Employee.from_dict(row))
            except (KeyError, TypeError, ValueError) as exc:
                raise DataFileError(f"Invalid employee record in {self.JSON_FILE}: {exc}") from exc

    def _save(self):
        write_json(self.JSON_FILE, [employee.to_dict() for employee in self.employees])

    def add_employee(self, employee_id, name, email, department, salary):
        data = validate_employee_data(employee_id, name, email, department, salary)
        if any(e.employee_id.casefold() == data["employee_id"].casefold()
               for e in self.employees):
            raise DuplicateEmployeeError(
                f"Employee ID {data['employee_id']} already exists."
            )
        employee = Employee(**data)
        self.employees.append(employee)
        try:
            self._save()
        except Exception:
            self.employees.remove(employee)
            raise
        return employee

    def list_employees(self):
        return list(self.employees)

    def get_employee(self, employee_id):
        employee_id = str(employee_id).strip()
        for employee in self.employees:
            if employee.employee_id.casefold() == employee_id.casefold():
                return employee
        raise EmployeeNotFoundError(f"Employee ID {employee_id} not found.")

    def search_employees(self, query):
        if not isinstance(query, str) or not query.strip():
            raise ValidationError("Search query cannot be empty.")
        query = query.strip().casefold()
        results = [
            employee for employee in self.employees
            if query in employee.employee_id.casefold()
            or query in employee.name.casefold()
            or query in employee.email.casefold()
            or query in employee.department.casefold()
        ]
        return results

    def update_employee(self, employee_id, **changes):
        employee = self.get_employee(employee_id)
        old_data = employee.to_dict()
        data = validate_employee_data(
            changes.get("employee_id", employee.employee_id),
            changes.get("name", employee.name),
            changes.get("email", employee.email),
            changes.get("department", employee.department),
            changes.get("salary", employee.salary),
        )
        if data["employee_id"].casefold() != employee.employee_id.casefold():
            if any(e.employee_id.casefold() == data["employee_id"].casefold()
                   for e in self.employees):
                raise DuplicateEmployeeError(
                    f"Employee ID {data['employee_id']} already exists."
                )
        for key, value in data.items():
            setattr(employee, key, value)
        try:
            self._save()
        except Exception:
            for key, value in old_data.items():
                setattr(employee, key, value)
            raise
        return employee

    def delete_employee(self, employee_id):
        employee = self.get_employee(employee_id)
        self.employees.remove(employee)
        try:
            self._save()
        except Exception:
            self.employees.append(employee)
            raise
        return employee

    def import_json(self, filename):
        rows = read_json(filename)
        imported = 0
        for row in rows:
            employee = Employee.from_dict(row)
            self.add_employee(
                employee.employee_id, employee.name, employee.email,
                employee.department, employee.salary
            )
            imported += 1
        return imported

    def import_csv(self, filename):
        rows = read_csv(filename)
        imported = 0
        for row in rows:
            self.add_employee(
                row.get("employee_id", ""),
                row.get("name", ""),
                row.get("email", ""),
                row.get("department", ""),
                row.get("salary", ""),
            )
            imported += 1
        return imported

    def export_json(self, filename="employees.json"):
        write_json(filename, [employee.to_dict() for employee in self.employees])

    def export_csv(self, filename="employees.csv"):
        from employee_app.file_handler import write_csv
        records = [employee.to_dict() for employee in self.employees]
        fields = ["employee_id", "name", "email", "department", "salary"]
        write_csv(filename, records, fields)
