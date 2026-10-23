
from datetime import date


def generate_library_report(book_service, loan_service):
    books = book_service.list_books()
    active_loans = loan_service.list_active_loans()

    total_books = sum(book.quantity for book in books)
    available_books = sum(
        book.available_copies for book in books
    )

    return {
        "total_book_titles": len(books),
        "total_book_copies": total_books,
        "available_copies": available_books,
        "issued_copies": total_books - available_books,
        "active_loans": len(active_loans),
        "report_date": date.today().isoformat(),
    }


def display_library_report(book_service, loan_service):
    report = generate_library_report(
        book_service, loan_service
    )

    print("\n======= LIBRARY REPORT =======")
    for key, value in report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("==============================")
