
def generate_report(employees):
    department_counts = {}
    total_salary = 0

    for employee in employees:
        department = employee.get("department", "Unknown")
        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )
        total_salary += employee["salary"]

    return {
        "total_employees": len(employees),
        "department_counts": department_counts,
        "total_salary": total_salary,
    }
