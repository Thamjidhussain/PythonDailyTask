from dataclasses import dataclass


@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    salary: float

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self.salary,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            employee_id=str(data["employee_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            department=str(data["department"]),
            salary=float(data["salary"]),
        )
