# Library Management System

A modular command-line Python project demonstrating object-oriented programming, JSON storage, input validation, exception handling, and reporting.

## Features

- Add, update, delete, and search books.
- Track book availability.
- Register, update, delete, and validate members.
- Issue and return books.
- Calculate late fines (default: Rs. 5 per late day; default loan: 14 days).
- Report available/borrowed books, top borrowers, and fines.
- Persist data in `data/books.json`, `data/members.json`, and `data/issues.json`.

## Requirements

- Python 3.10 or newer (uses built-in type hints and dataclasses).
- No third-party packages required.

## Run

Open a terminal in the `library_management` folder:

```powershell
py app.py
```

The JSON data files are initialized automatically if they do not exist. The included files contain empty lists, so the project starts with no books or members.

## Suggested manual test

1. Choose `1` and add book `B001`, title `Python Basics`, author `A. Writer`, year `2024`.
2. Choose `5` and register member `M001`, name `Demo Member`, email `demo@example.com`.
3. Choose `9` and issue `I001` for book `B001` to member `M001`.
4. Choose `2` to verify the book is marked Borrowed.
5. Choose `10` and return `I001`. To test late fines deterministically, use the `IssueManager` from Python with an explicit date (see example below).
6. Choose `11` to view reports.

## Test a late fine from Python

The interactive app uses today's date. To test a predictable overdue return, run this snippet from the project folder after adding the sample book/member (or use fresh JSON data):

```python
from datetime import date
from book import BookManager
from member import MemberManager
from issue import IssueManager

books = BookManager()
members = MemberManager()
issues = IssueManager(books, members, loan_days=14, fine_per_day=5)

issues.issue_book("I-DEMO", "B001", "M001", on_date=date(2026, 1, 1))
record = issues.return_book("I-DEMO", on_date=date(2026, 1, 20))
print(record.fine)  # 25.0: five late days x Rs. 5
```

Use unique IDs when running the snippet; issue IDs are not reusable.

## Modules

- `book.py`: `Book` model and `BookManager`
- `member.py`: `Member` model and `MemberManager`
- `issue.py`: `IssueRecord` and `IssueManager`
- `reports.py`: report generation
- `storage.py`: JSON read/write helpers
- `validator.py`: validation helpers
- `exceptions.py`: custom exceptions
- `app.py`: command-line menu

## Design notes

- `IssueManager` uses composition: it receives `BookManager` and `MemberManager` objects.
- `Book` and `Member` are data models; manager classes own catalogue operations.
- Invalid input and missing records raise custom exceptions that the CLI catches.
- This is an educational single-user application. For production use, add transaction-safe writes, authentication, stronger email validation, and safeguards against deleting members with active loans.
