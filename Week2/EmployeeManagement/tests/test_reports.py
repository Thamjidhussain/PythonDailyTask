from employee_app.employee_service import EmployeeService
from employee_app.reports import department_report


def test_department_report(tmp_path, monkeypatch):
    import employee_app.file_handler as fh
    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    service = EmployeeService()
    service.add_employee("E101", "Rahul", "rahul@example.com", "IT", 45000)
    service.add_employee("E102", "Arjun", "arjun@example.com", "IT", 52000)
    service.add_employee("E103", "Priya", "priya@example.com", "HR", 38000)

    report = department_report(service)
    assert report["IT"]["employee_count"] == 2
    assert report["IT"]["average_salary"] == 48500
    assert report["HR"]["average_salary"] == 38000
