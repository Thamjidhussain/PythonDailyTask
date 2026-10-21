
from pathlib import Path

from parser import parse_json
from validator import validate_employees
from processor import generate_report


def main():
    input_file = Path(__file__).with_name("sample.json")

    try:
        json_text = input_file.read_text(encoding="utf-8")
        employees = parse_json(json_text)
        validate_employees(employees)
        report = generate_report(employees)

        print("Validation successful")
        print("Report:", report)

    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
