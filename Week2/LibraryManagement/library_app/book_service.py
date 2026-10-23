
from library_app.models import Book
from library_app.file_handler import read_json, write_json
from library_app.validators import (
    BookNotFoundError,
    DuplicateRecordError,
    ValidationError,
    validate_id,
    validate_quantity,
    validate_text,
)


class BookService:
    FILE = "books.json"

    def __init__(self):
        self.books = [
            Book.from_dict(item)
            for item in read_json(self.FILE)
        ]

    def _save(self):
        write_json(
            self.FILE,
            [book.to_dict() for book in self.books],
        )

    def add_book(self, book_id, title, author, quantity):
        book_id = validate_id(book_id, "Book ID")
        title = validate_text(title, "Title")
        author = validate_text(author, "Author")
        quantity = validate_quantity(quantity)

        if any(book.book_id == book_id for book in self.books):
            raise DuplicateRecordError(
                f"Book ID {book_id} already exists."
            )

        book = Book(book_id, title, author, quantity, quantity)
        self.books.append(book)

        try:
            self._save()
        except Exception:
            self.books.remove(book)
            raise

        return book

    def list_books(self):
        return list(self.books)

    def search_book(self, query):
        query = validate_text(query, "Search query").casefold()

        results = [
            book for book in self.books
            if query in book.book_id.casefold()
            or query in book.title.casefold()
            or query in book.author.casefold()
        ]

        if not results:
            raise BookNotFoundError(
                f"No books found for '{query}'."
            )

        return results

    def get_book(self, book_id):
        book_id = validate_id(book_id, "Book ID")

        for book in self.books:
            if book.book_id == book_id:
                return book

        raise BookNotFoundError(
            f"Book ID {book_id} not found."
        )

    def update_book(self, book_id, title=None, author=None):
        book = self.get_book(book_id)

        if title is not None:
            book.title = validate_text(title, "Title")

        if author is not None:
            book.author = validate_text(author, "Author")

        self._save()
        return book

    def delete_book(self, book_id):
        book = self.get_book(book_id)

        if book.available_copies != book.quantity:
            raise ValidationError(
                "Cannot delete a book with active loans."
            )

        self.books.remove(book)
        self._save()
        return True
