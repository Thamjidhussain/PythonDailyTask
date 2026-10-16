
from dataclasses import dataclass


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    quantity: int
    available_copies: int

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "quantity": self.quantity,
            "available_copies": self.available_copies,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Member:
    member_id: str
    name: str
    email: str

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Loan:
    loan_id: str
    book_id: str
    member_id: str
    issue_date: str
    due_date: str
    return_date: str = ""

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
