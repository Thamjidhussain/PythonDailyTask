"""Book model and book catalogue operations."""
from dataclasses import dataclass, asdict
from typing import Optional
from exceptions import NotFoundError, ValidationError
from storage import load_records, save_records
from validator import require_text


@dataclass
class Book:
    """Represent a book in the library."""
    book_id: str
    title: str
    author: str
    year: int
    available: bool = True

    def to_dict(self) -> dict:
        """Convert the book into a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Create a Book from stored dictionary data."""
        return cls(**data)


class BookManager:
    """Manage the library's book catalogue."""
    FILE = "books.json"

    def __init__(self) -> None:
        """Load books from JSON storage."""
        self.books = [Book.from_dict(row) for row in load_records(self.FILE)]

    def _save(self) -> None:
        """Persist the current catalogue."""
        save_records(self.FILE, [book.to_dict() for book in self.books])

    def list_books(self) -> list[Book]:
        """Return all books."""
        return list(self.books)

    def get(self, book_id: str) -> Book:
        """Find a book by its ID."""
        for book in self.books:
            if book.book_id == book_id:
                return book
        raise NotFoundError(f"Book '{book_id}' was not found.")

    def add(self, book_id: str, title: str, author: str, year: int) -> Book:
        """Add a new book after validating its fields."""
        book_id = require_text(book_id, "Book ID")
        title = require_text(title, "Title")
        author = require_text(author, "Author")
        if isinstance(year, bool) or not isinstance(year, int) or not 0 < year <= 9999:
            raise ValidationError("Year must be a valid positive year.")
        if any(book.book_id == book_id for book in self.books):
            raise ValidationError(f"Book ID '{book_id}' already exists.")
        book = Book(book_id, title, author, year)
        self.books.append(book)
        self._save()
        return book

    def update(self, book_id: str, title: Optional[str] = None,
               author: Optional[str] = None, year: Optional[int] = None) -> Book:
        """Update supplied book fields."""
        book = self.get(book_id)
        if title is not None:
            book.title = require_text(title, "Title")
        if author is not None:
            book.author = require_text(author, "Author")
        if year is not None:
            if isinstance(year, bool) or not isinstance(year, int) or not 0 < year <= 9999:
                raise ValidationError("Year must be a valid positive year.")
            book.year = year
        self._save()
        return book

    def delete(self, book_id: str) -> None:
        """Delete a book that is not currently borrowed."""
        book = self.get(book_id)
        if not book.available:
            raise ValidationError("Cannot delete a borrowed book. Return it first.")
        self.books.remove(book)
        self._save()

    def search(self, query: str) -> list[Book]:
        """Search titles and authors case-insensitively."""
        query = require_text(query, "Search query").casefold()
        return [book for book in self.books
                if query in book.title.casefold() or query in book.author.casefold()]
