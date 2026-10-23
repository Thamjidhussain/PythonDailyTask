# Day 3 - Employee CSV/JSON Report

## Project Overview

This project is a Python employee reporting application that reads employee data from a CSV file, validates the records, generates department-wise statistics, identifies recently joined employees, and exports the results to CSV and JSON files.

The project also handles invalid data without crashing the program.

## Technologies Used

- Python
- CSV module
- JSON module
- pathlib
- os
- datetime
- pytest

## Input File

The main input file is:

```text
employees.csv
```

It contains the following columns:

```text
name
department
salary
join_date
```

The file contains 50+ employee records.

## Main Features

### 1. CSV Processing

The program reads employee information from `employees.csv` using Python's built-in `csv` module.

### 2. Data Validation

The program validates each employee record.

It detects:

- Blank rows
- Missing values
- Non-numeric salaries
- Invalid date formats
- Duplicate rows

Invalid records are not processed further.

Instead, they are written to:

```text
rejected.csv
```

### 3. Department Statistics

The program calculates:

- Department-wise headcount
- Department-wise average salary

Example:

```text
IT       Headcount: 10    Average Salary: ₹75000
HR       Headcount: 8     Average Salary: ₹55000
Finance  Headcount: 12    Average Salary: ₹70000
```

### 4. Recently Joined Employees

The program identifies employees who joined within the last 90 days.

This calculation uses Python's `datetime` and `timedelta`.

### 5. CSV Export

The department report is exported to:

```text
employees_report.csv
```

### 6. JSON Export

The complete report is exported to:

```text
employees_report.json
```

### 7. Batch Processing

The project uses `pathlib` to find CSV files inside a folder.

This allows the application to be extended to process multiple CSV files.

## Project Structure

```text
Day3/
│
├── employees.csv
├── employee_report.py
├── test_employee_report.py
├── README.md
│
├── employees_report.csv
├── employees_report.json
└── rejected.csv
```

## How to Run

Open the terminal inside the `Day3` directory.

Run:

```bash
python employee_report.py
```

The program will generate:

```text
employees_report.csv
employees_report.json
rejected.csv
```

## Running Tests

Install pytest if required:

```bash
python -m pip install pytest
```

Run all tests:

```bash
python -m pytest -v
```

The project contains 10 test cases covering:

- Valid dates
- Invalid dates
- Valid employee records
- Non-numeric salaries
- Missing values
- Duplicate records
- Department statistics
- Recently joined employees
- Rejected CSV generation
- Blank rows

## Error Handling

Bad data should not cause the entire program to crash.

For example:

```csv
John Test,IT,abc,2026-08-01
```

The salary is not numeric, so the record is rejected and written to:

```text
rejected.csv
```

with the reason:

```text
Non-numeric salary
```

## Completion Criteria

The project is considered complete when:

- [x] CSV data can be read
- [x] JSON export is implemented
- [x] CSV export is implemented
- [x] Department headcount is calculated
- [x] Average salary is calculated
- [x] Last 90 days filtering is implemented
- [x] Duplicate records are detected
- [x] Missing values are detected
- [x] Invalid dates are detected
- [x] Non-numeric salaries are rejected
- [x] Rejected records are logged
- [x] Blank rows are handled
- [x] Pytest cases are implemented
- [ ] Manual 10-row calculation is verified
- [ ] Git commit is completed

## Git Commit

After testing and verification, use:

```bash
git add .
git commit -m "feat(day3): CSV/JSON employee report with validation"
```

Then check:

```bash
git status
```

The working tree should be clean after the commit.

## Learning Outcomes

By completing this project, I practiced:

- Reading and writing CSV files
- Creating JSON reports
- Using `pathlib`
- Using `os`
- Working with `datetime`
- List and dictionary comprehensions
- Sorting data
- Grouping data
- Data validation
- Exception handling
- File processing
- Unit testing with pytest
- Git version control