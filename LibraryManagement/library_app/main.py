
import logging

from library_app.book_service import BookService
from library_app.member_service import MemberService
from library_app.loan_service import LoanService
from library_app.reports import display_library_report
from library_app.validators import LibraryError


def setup_logging():
    from pathlib import Path

    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "library.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()

    try:
        books = BookService()
        members = MemberService()
        loans = LoanService(books, members)
    except (LibraryError, ValueError, TypeError) as exc:
        logging.exception("Application initialization failed")
        print(f"Unable to start: {exc}")
        return

    while True:
        print("""
======= LIBRARY MANAGEMENT =======
1. Add Book
2. List Books
3. Search Book
4. Register Member
5. List Members
6. Issue Book
7. Return Book
8. List Active Loans
9. Library Report
0. Exit
==================================
""")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                book = books.add_book(
                    input("Book ID: "),
                    input("Title: "),
                    input("Author: "),
                    int(input("Quantity: ")),
                )
                print(f"Book added: {book.title}")
                logging.info("Book added: %s", book.book_id)

            elif choice == "2":
                for book in books.list_books():
                    print(book)

            elif choice == "3":
                for book in books.search_book(
                    input("Enter title, author, or ID: ")
                ):
                    print(book)

            elif choice == "4":
                member = members.register_member(
                    input("Member ID: "),
                    input("Name: "),
                    input("Email: "),
                )
                print(f"Member registered: {member.name}")
                logging.info(
                    "Member registered: %s", member.member_id
                )

            elif choice == "5":
                for member in members.list_members():
                    print(member)

            elif choice == "6":
                loan = loans.issue_book(
                    input("Loan ID: "),
                    input("Book ID: "),
                    input("Member ID: "),
                )
                print(f"Book issued. Due date: {loan.due_date}")
                logging.info("Loan created: %s", loan.loan_id)

            elif choice == "7":
                fine = loans.return_book(input("Loan ID: "))
                print(f"Book returned. Fine: Rs. {fine}")
                logging.info("Book returned")

            elif choice == "8":
                for loan in loans.list_active_loans():
                    print(loan)

            elif choice == "9":
                display_library_report(books, loans)

            elif choice == "0":
                print("Thank you for using the Library System.")
                break

            else:
                print("Invalid choice. Try again.")

        except (LibraryError, ValueError, TypeError) as exc:
            logging.warning("Operation failed: %s", exc)
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
