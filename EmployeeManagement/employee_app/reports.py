from collections import defaultdict


def department_report(employee_service):
    grouped = defaultdict(list)
    for employee in employee_service.list_employees():
        grouped[employee.department].append(employee.salary)

    report = {}
    for department, salaries in sorted(grouped.items()):
        report[department] = {
            "employee_count": len(salaries),
            "average_salary": round(sum(salaries) / len(salaries), 2),
            "total_salary": round(sum(salaries), 2),
        }
    return report


def print_department_report(employee_service):
    report = department_report(employee_service)
    print("\n========== DEPARTMENT REPORT ==========")
    if not report:
        print("No employee records available.")
    for department, values in report.items():
        print(
            f"{department}: {values['employee_count']} employees | "
            f"Average salary: Rs. {values['average_salary']:.2f} | "
            f"Total salary: Rs. {values['total_salary']:.2f}"
        )
    print("=======================================")
    return report
