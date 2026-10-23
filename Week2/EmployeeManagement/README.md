# Employee Data Management System

A Python command-line mini-project for managing employee records, importing/exporting CSV and JSON, validating input, and generating department salary reports.

## Requirements
- Python 3.10+
- pip

## Setup (Windows PowerShell)

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    py -m pip install -r requirements.txt

## Run tests

    py -m pytest -v

## Run application

    py -m employee_app.main

## Data
Sample employees are stored in `data/employees.json` and `data/employees.csv`.
Application logs are written to `logs/employee.log`.

## Team responsibilities
- Thamzid Hussain Shaik Gaffar: modules, packages, dependency setup
- Bhuvaneswari Galam: exceptions, file handling, validation
- Thupakula Divya: pytest coverage, integration, final demo
