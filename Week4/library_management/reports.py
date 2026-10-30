"""Library reporting functions."""
from collections import Counter
from book import BookManager
from member import MemberManager
from issue import IssueManager


class ReportManager:
    """Generate availability, borrower, and fine reports."""

    def __init__(self, books: BookManager, members: MemberManager,
                 issues: IssueManager) -> None:
        """Store the managers needed to create reports."""
        self.books = books
        self.members = members
        self.issues = issues

    def available_books(self) -> list:
        """List books currently available to borrow."""
        return [book for book in self.books.list_books() if book.available]

    def borrowed_books(self) -> list:
        """List books currently on loan."""
        return [book for book in self.books.list_books() if not book.available]

    def top_borrowers(self, limit: int = 5) -> list[tuple[str, int]]:
        """Return member IDs and issue counts, highest first."""
        counts = Counter(issue.member_id for issue in self.issues.list_issues())
        return counts.most_common(max(0, limit))

    def fine_report(self) -> list[dict]:
        """List loans with fines and the total recorded fines."""
        rows = [
            {"issue_id": issue.issue_id, "member_id": issue.member_id,
             "book_id": issue.book_id, "fine": issue.fine,
             "return_date": issue.return_date}
            for issue in self.issues.list_issues() if issue.fine > 0
        ]
        rows.append({"total_fines": round(sum(row["fine"] for row in rows), 2)})
        return rows
