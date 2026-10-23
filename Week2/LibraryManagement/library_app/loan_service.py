
from datetime import date, timedelta

from library_app.models import Loan
from library_app.file_handler import read_json, write_json
from library_app.validators import (
    BookUnavailableError,
    DuplicateRecordError,
    LibraryError,
    validate_id,
)


class LoanService:
    FILE = "loans.json"
    LOAN_DAYS = 14
    FINE_PER_DAY = 5

    def __init__(self, book_service, member_service):
        self.book_service = book_service
        self.member_service = member_service
        self.loans = [
            Loan.from_dict(item)
            for item in read_json(self.FILE)
        ]

    def _save(self):
        write_json(
            self.FILE,
            [loan.to_dict() for loan in self.loans],
        )

    def issue_book(self, loan_id, book_id, member_id):
        loan_id = validate_id(loan_id, "Loan ID")
        book_id = validate_id(book_id, "Book ID")
        member_id = validate_id(member_id, "Member ID")

        if any(loan.loan_id == loan_id for loan in self.loans):
            raise DuplicateRecordError(
                f"Loan ID {loan_id} already exists."
            )

        book = self.book_service.get_book(book_id)
        self.member_service.get_member(member_id)

        if book.available_copies <= 0:
            raise BookUnavailableError(
                f"Book {book_id} is not available."
            )

        today = date.today()
        loan = Loan(
            loan_id=loan_id,
            book_id=book_id,
            member_id=member_id,
            issue_date=today.isoformat(),
            due_date=(today + timedelta(
                days=self.LOAN_DAYS
            )).isoformat(),
        )

        book.available_copies -= 1
        self.loans.append(loan)

        try:
            self.book_service._save()
            self._save()
        except Exception:
            self.loans.remove(loan)
            book.available_copies += 1
            self.book_service._save()
            raise

        return loan

    def return_book(self, loan_id):
        loan_id = validate_id(loan_id, "Loan ID")

        loan = next(
            (
                item for item in self.loans
                if item.loan_id == loan_id
            ),
            None,
        )

        if loan is None:
            raise LibraryError(
                f"Loan ID {loan_id} not found."
            )

        if loan.return_date:
            raise LibraryError(
                "This book has already been returned."
            )

        book = self.book_service.get_book(loan.book_id)

        loan.return_date = date.today().isoformat()
        book.available_copies += 1

        try:
            self.book_service._save()
            self._save()
        except Exception:
            loan.return_date = ""
            book.available_copies -= 1
            self.book_service._save()
            raise

        return self.calculate_fine(loan)

    def calculate_fine(self, loan):
        end_date = date.fromisoformat(
            loan.return_date or date.today().isoformat()
        )
        due_date = date.fromisoformat(loan.due_date)
        overdue_days = max(0, (end_date - due_date).days)

        return overdue_days * self.FINE_PER_DAY

    def list_active_loans(self):
        return [
            loan for loan in self.loans
            if not loan.return_date
        ]
