
import csv
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path


class ReportGenerator:
    """Generate employee reports from a CSV file."""

    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.employees = []

    def load_employees(self):
        """Read and validate employee records."""
        if not self.input_file.exists():
            raise FileNotFoundError(
                f"Employee file not found: {self.input_file}"
            )

        self.employees = []

        with self.input_file.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            required = {"name", "department", "salary", "join_date"}
            if not reader.fieldnames or not required.issubset(
                reader.fieldnames
            ):
                raise ValueError(
                    "CSV must contain: name, department, salary, join_date"
                )

            for row_number, row in enumerate(reader, start=2):
                try:
                    name = (row.get("name") or "").strip()
                    department = (row.get("department") or "").strip()
                    salary_text = (row.get("salary") or "").strip()
                    join_date_text = (row.get("join_date") or "").strip()

                    if not all(
                        [name, department, salary_text, join_date_text]
                    ):
                        raise ValueError("Missing required value")

                    salary = float(salary_text)
                    if salary < 0:
                        raise ValueError("Salary cannot be negative")

                    join_date = date.fromisoformat(join_date_text)

                    self.employees.append(
                        {
                            "name": name,
                            "department": department,
                            "salary": salary,
                            "join_date": join_date.isoformat(),
                        }
                    )

                except (ValueError, TypeError) as error:
                    print(
                        f"Skipping invalid CSV row {row_number}: {error}"
                    )

        return self.employees

    def department_statistics(self):
        """Calculate employee count and average salary by department."""
        if not self.employees:
            self.load_employees()

        departments = defaultdict(list)

        for employee in self.employees:
            departments[employee["department"]].append(
                employee["salary"]
            )

        statistics = {}

        for department, salaries in sorted(departments.items()):
            statistics[department] = {
                "employee_count": len(salaries),
                "average_salary": round(
                    sum(salaries) / len(salaries), 2
                ),
            }

        return statistics

    def employees_joined_last_90_days(self):
        """Find employees who joined within the last 90 days."""
        if not self.employees:
            self.load_employees()

        today = date.today()
        cutoff = today - timedelta(days=90)

        return [
            employee
            for employee in self.employees
            if cutoff
            <= date.fromisoformat(employee["join_date"])
            <= today
        ]

    def generate_report(self, output_file="employee_report.json"):
        """Save employee statistics and recent joiners to JSON."""
        if not self.employees:
            self.load_employees()

        report = {
            "total_employees": len(self.employees),
            "department_statistics": self.department_statistics(),
            "employees_joined_last_90_days": (
                self.employees_joined_last_90_days()
            ),
        }

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return report
