"""Book issue/return workflows, due dates, and fines."""
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from typing import Optional
from exceptions import AvailabilityError, NotFoundError, ValidationError
from storage import load_records, save_records
from book import BookManager
from member import MemberManager
from validator import require_text, parse_date


@dataclass
class IssueRecord:
    """Track a book loan."""
    issue_id: str
    book_id: str
    member_id: str
    issue_date: str
    due_date: str
    return_date: Optional[str] = None
    fine: float = 0.0

    def to_dict(self) -> dict:
        """Convert the issue record to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "IssueRecord":
        """Create an issue record from stored data."""
        return cls(**data)


class IssueManager:
    """Coordinate book and member objects to manage loans."""
    FILE = "issues.json"

    def __init__(self, books: BookManager, members: MemberManager,
                 loan_days: int = 14, fine_per_day: float = 5.0) -> None:
        """Load loans and store the collaborating managers."""
        if loan_days <= 0 or fine_per_day < 0:
            raise ValidationError("Loan days must be positive and fine cannot be negative.")
        self.books = books
        self.members = members
        self.loan_days = loan_days
        self.fine_per_day = fine_per_day
        self.issues = [IssueRecord.from_dict(row) for row in load_records(self.FILE)]

    def _save(self) -> None:
        """Persist all issue records."""
        save_records(self.FILE, [record.to_dict() for record in self.issues])

    def issue_book(self, issue_id: str, book_id: str, member_id: str,
                   on_date: Optional[date] = None) -> IssueRecord:
        """Issue an available book to an active member."""
        issue_id = require_text(issue_id, "Issue ID")
        book = self.books.get(book_id)
        self.members.validate(member_id)
        if not book.available:
            raise AvailabilityError("This book is already borrowed.")
        if any(record.issue_id == issue_id for record in self.issues):
            raise ValidationError(f"Issue ID '{issue_id}' already exists.")
        today = on_date or date.today()
        due = today + timedelta(days=self.loan_days)
        record = IssueRecord(issue_id, book_id, member_id,
                             today.isoformat(), due.isoformat())
        book.available = False
        self.books._save()
        self.issues.append(record)
        self._save()
        return record

    def return_book(self, issue_id: str,
                    on_date: Optional[date] = None) -> IssueRecord:
        """Return a borrowed book and calculate any late fine."""
        record = next((item for item in self.issues
                       if item.issue_id == issue_id), None)
        if record is None:
            raise NotFoundError(f"Issue '{issue_id}' was not found.")
        if record.return_date is not None:
            raise AvailabilityError("This issue has already been returned.")
        returned = on_date or date.today()
        due = parse_date(record.due_date)
        if returned < parse_date(record.issue_date):
            raise ValidationError("Return date cannot be before issue date.")
        late_days = max(0, (returned - due).days)
        record.return_date = returned.isoformat()
        record.fine = round(late_days * self.fine_per_day, 2)
        self.books.get(record.book_id).available = True
        self.books._save()
        self._save()
        return record

    def list_issues(self) -> list[IssueRecord]:
        """Return all loan records."""
        return list(self.issues)
