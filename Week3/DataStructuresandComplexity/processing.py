
from collections import deque


def process_employees(employees):
    employee_list = []
    employee_dict = {}
    employee_set = set()
    employee_queue = deque()
    duplicates = []

    for employee in employees:
        employee_id = employee.get("id")

        if employee_id is None or employee_id == "":
            raise ValueError("Employee ID cannot be empty")

        if employee_id in employee_set:
            duplicates.append(employee_id)
            continue

        employee_set.add(employee_id)
        employee_list.append(employee)
        employee_dict[employee_id] = employee
        employee_queue.append(employee_id)

    processed_ids = []

    while employee_queue:
        processed_ids.append(employee_queue.popleft())

    return {
        "employees": employee_list,
        "employee_index": employee_dict,
        "duplicates": duplicates,
        "processed_ids": processed_ids,
    }
if __name__ == "__main__":
    employees = [
        {"id": "E101", "name": "Asha"},
        {"id": "E102", "name": "Rahul"},
        {"id": "E101", "name": "Duplicate"},
    ]

    result = process_employees(employees)

    print("Employee Records:", result["employees"])
    print("Employee Index:", result["employee_index"])
    print("Duplicate IDs:", result["duplicates"])
    print("Processed IDs:", result["processed_ids"])