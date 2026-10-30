"""Member model and member registration operations."""
from dataclasses import dataclass, asdict
from exceptions import NotFoundError, ValidationError
from storage import load_records, save_records
from validator import require_text


@dataclass
class Member:
    """Represent a registered library member."""
    member_id: str
    name: str
    email: str
    active: bool = True

    def to_dict(self) -> dict:
        """Convert the member into a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        """Create a Member from stored dictionary data."""
        return cls(**data)


class MemberManager:
    """Register, update, validate, and remove members."""
    FILE = "members.json"

    def __init__(self) -> None:
        """Load members from JSON storage."""
        self.members = [Member.from_dict(row) for row in load_records(self.FILE)]

    def _save(self) -> None:
        """Persist the current member list."""
        save_records(self.FILE, [member.to_dict() for member in self.members])

    def list_members(self) -> list[Member]:
        """Return all members."""
        return list(self.members)

    def get(self, member_id: str) -> Member:
        """Find a member by ID."""
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise NotFoundError(f"Member '{member_id}' was not found.")

    def validate(self, member_id: str) -> Member:
        """Return an active member or reject the membership."""
        member = self.get(member_id)
        if not member.active:
            raise ValidationError("This membership is inactive.")
        return member

    def register(self, member_id: str, name: str, email: str) -> Member:
        """Register a new member."""
        member_id = require_text(member_id, "Member ID")
        name = require_text(name, "Name")
        email = require_text(email, "Email")
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValidationError("Enter a valid email address.")
        if any(member.member_id == member_id for member in self.members):
            raise ValidationError(f"Member ID '{member_id}' already exists.")
        member = Member(member_id, name, email)
        self.members.append(member)
        self._save()
        return member

    def update(self, member_id: str, name: str, email: str,
               active: bool = True) -> Member:
        """Update a member's name, email, and active status."""
        member = self.get(member_id)
        member.name = require_text(name, "Name")
        email = require_text(email, "Email")
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValidationError("Enter a valid email address.")
        member.email = email
        member.active = bool(active)
        self._save()
        return member

    def delete(self, member_id: str) -> None:
        """Delete a member record."""
        member = self.get(member_id)
        self.members.remove(member)
        self._save()
