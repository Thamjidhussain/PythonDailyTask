
import pytest

from library_app.book_service import BookService
from library_app.validators import (
    DuplicateRecordError,
    BookNotFoundError,
)


@pytest.fixture
def service(tmp_path, monkeypatch):
    import library_app.file_handler as fh

    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    return BookService()


def test_add_book(service):
    book = service.add_book(
        "B101", "Python Basics", "John Smith", 3
    )

    assert book.title == "Python Basics"
    assert book.available_copies == 3


def test_duplicate_book_rejected(service):
    service.add_book("B101", "Python", "John", 2)

    with pytest.raises(DuplicateRecordError):
        service.add_book("B101", "Java", "Mary", 1)


def test_search_missing_book(service):
    with pytest.raises(BookNotFoundError):
        service.search_book("Unknown")
