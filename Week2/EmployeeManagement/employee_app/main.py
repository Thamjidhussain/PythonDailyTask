import logging
from pathlib import Path

from employee_app.employee_service import EmployeeService
from employee_app.reports import print_department_report
from employee_app.validators import EmployeeAppError


def setup_logging():
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "employee.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def show_employee(employee):
    print(
        f"{employee.employee_id} | {employee.name} | {employee.email} | "
        f"{employee.department} | Rs. {employee.salary:.2f}"
    )


def main():
    setup_logging()
    try:
        service = EmployeeService()
    except EmployeeAppError as exc:
        print(f"Could not load employee data: {exc}")
        logging.exception("Application startup failed")
        return

    while True:
        print("""
====== EMPLOYEE DATA MANAGEMENT ======
1. Add Employee
2. View All Employees
3. Search Employee
4. Update Employee
5. Delete Employee
6. Import CSV
7. Import JSON
8. Export JSON
9. Export CSV
10. Department Salary Report
0. Exit
======================================
""")
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                employee = service.add_employee(
                    input("Employee ID: "),
                    input("Name: "),
                    input("Email: "),
                    input("Department: "),
                    input("Salary: "),
                )
                print(f"Employee added successfully: {employee.name}")
                logging.info("Employee added: %s", employee.employee_id)
            elif choice == "2":
                employees = service.list_employees()
                if not employees:
                    print("No employee records found.")
                for employee in employees:
                    show_employee(employee)
            elif choice == "3":
                results = service.search_employees(input("Search by ID/name/email/department: "))
                if not results:
                    print("No matching employees found.")
                for employee in results:
                    show_employee(employee)
            elif choice == "4":
                employee_id = input("Employee ID to update: ")
                employee = service.get_employee(employee_id)
                print("Press Enter to keep the current value.")
                name = input(f"Name [{employee.name}]: ").strip() or employee.name
                email = input(f"Email [{employee.email}]: ").strip() or employee.email
                department = input(f"Department [{employee.department}]: ").strip() or employee.department
                salary_text = input(f"Salary [{employee.salary}]: ").strip()
                salary = salary_text if salary_text else employee.salary
                updated = service.update_employee(
                    employee_id, name=name, email=email,
                    department=department, salary=salary
                )
                print(f"Updated employee: {updated.name}")
                logging.info("Employee updated: %s", updated.employee_id)
            elif choice == "5":
                employee_id = input("Employee ID to delete: ")
                deleted = service.delete_employee(employee_id)
                print(f"Deleted employee: {deleted.name}")
                logging.info("Employee deleted: %s", deleted.employee_id)
            elif choice == "6":
                filename = input("CSV filename in data folder [employees.csv]: ").strip() or "employees.csv"
                count = service.import_csv(filename)
                print(f"Imported {count} employee(s) from CSV.")
                logging.info("Imported %s CSV employees from %s", count, filename)
            elif choice == "7":
                filename = input("JSON filename in data folder [employees.json]: ").strip() or "employees.json"
                count = service.import_json(filename)
                print(f"Imported {count} employee(s) from JSON.")
                logging.info("Imported %s JSON employees from %s", count, filename)
            elif choice == "8":
                filename = input("Output JSON filename [employees.json]: ").strip() or "employees.json"
                service.export_json(filename)
                print(f"Exported {len(service.list_employees())} employee(s) to {filename}.")
            elif choice == "9":
                filename = input("Output CSV filename [employees.csv]: ").strip() or "employees.csv"
                service.export_csv(filename)
                print(f"Exported {len(service.list_employees())} employee(s) to {filename}.")
            elif choice == "10":
                print_department_report(service)
            elif choice == "0":
                print("Thank you for using Employee Data Management System.")
                break
            else:
                print("Invalid choice. Enter a number from 0 to 10.")
        except (EmployeeAppError, ValueError, TypeError) as exc:
            logging.warning("Operation failed: %s", exc)
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
