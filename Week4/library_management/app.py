"""Command-line entry point for the Library Management System."""
from exceptions import LibraryError
from book import BookManager
from member import MemberManager
from issue import IssueManager
from reports import ReportManager


def show_books(manager: BookManager) -> None:
    """Print all books in a compact format."""
    books = manager.list_books()
    if not books:
        print("No books found.")
    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(f"{book.book_id}: {book.title} by {book.author} ({book.year}) - {status}")


def main() -> None:
    """Run the interactive library menu."""
    books = BookManager()
    members = MemberManager()
    issues = IssueManager(books, members)
    reports = ReportManager(books, members, issues)

    while True:
        print("=== Library Management System ===")
        print("1. Add book")
        print("2. List/search books")
        print("3. Update book")
        print("4. Delete book")
        print("5. Register member")
        print("6. List members")
        print("7. Update member")
        print("8. Delete member")
        print("9. Issue book")
        print("10. Return book")
        print("11. Reports")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                books.add(input("Book ID: "), input("Title: "),
                          input("Author: "), int(input("Publication year: ")))
                print("Book added.")
            elif choice == "2":
                query = input("Search title/author (leave blank to list all): ").strip()
                results = books.list_books() if not query else books.search(query)
                if not results:
                    print("No matching books.")
                for book in results:
                    status = "Available" if book.available else "Borrowed"
                    print(f"{book.book_id}: {book.title} by {book.author} "
                          f"({book.year}) - {status}")
            elif choice == "3":
                book_id = input("Book ID to update: ").strip()
                title = input("New title (blank to keep current): ").strip() or None
                author = input("New author (blank to keep current): ").strip() or None
                year_text = input("New year (blank to keep current): ").strip()
                year = int(year_text) if year_text else None
                books.update(book_id, title, author, year)
                print("Book updated.")
            elif choice == "4":
                books.delete(input("Book ID to delete: ").strip())
                print("Book deleted.")
            elif choice == "5":
                members.register(input("Member ID: "), input("Name: "), input("Email: "))
                print("Member registered.")
            elif choice == "6":
                for member in members.list_members():
                    status = "Active" if member.active else "Inactive"
                    print(f"{member.member_id}: {member.name} | {member.email} | {status}")
                if not members.list_members():
                    print("No members registered.")
            elif choice == "7":
                member_id = input("Member ID: ").strip()
                name = input("New name: ")
                email = input("New email: ")
                active_text = input("Active? (y/n): ").strip().lower()
                members.update(member_id, name, email, active_text == "y")
                print("Member updated.")
            elif choice == "8":
                members.delete(input("Member ID to delete: ").strip())
                print("Member deleted.")
            elif choice == "9":
                issues.issue_book(input("Issue ID: "), input("Book ID: "),
                                  input("Member ID: "))
                print("Book issued.")
            elif choice == "10":
                record = issues.return_book(input("Issue ID: ").strip())
                print(f"Book returned. Fine: Rs.{record.fine:.2f}")
            elif choice == "11":
                print("\\nAvailable books:")
                for book in reports.available_books():
                    print(f"- {book.book_id}: {book.title}")
                print("Borrowed books:")
                for book in reports.borrowed_books():
                    print(f"- {book.book_id}: {book.title}")
                print("Top borrowers (member ID, number of loans):")
                print(reports.top_borrowers())
                print("Fine report:")
                print(reports.fine_report())
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please choose a listed option.")
        except (ValueError, LibraryError) as exc:
            print(f"Error: {exc}")
        except OSError as exc:
            print(f"Storage error: {exc}")


if __name__ == "__main__":
    main()
