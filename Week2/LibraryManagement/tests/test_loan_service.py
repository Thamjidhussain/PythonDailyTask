
import pytest

from library_app.book_service import BookService
from library_app.member_service import MemberService
from library_app.loan_service import LoanService


@pytest.fixture
def setup_services(tmp_path, monkeypatch):
    import library_app.file_handler as fh

    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)

    books = BookService()
    members = MemberService()
    loans = LoanService(books, members)

    books.add_book("B101", "Python", "John", 1)
    members.register_member(
        "M001", "Alex", "alex@example.com"
    )

    return books, members, loans


def test_issue_and_return_book(setup_services):
    books, _, loans = setup_services

    loan = loans.issue_book("L001", "B101", "M001")

    assert books.get_book("B101").available_copies == 0
    assert loan.return_date == ""

    loans.return_book("L001")

    assert books.get_book("B101").available_copies == 1
    assert loan.return_date != ""


def test_cannot_issue_unavailable_book(setup_services):
    books, _, loans = setup_services

    loans.issue_book("L001", "B101", "M001")

    with pytest.raises(Exception):
        loans.issue_book("L002", "B101", "M001")

    assert books.get_book("B101").available_copies == 0
