
from library_app.models import Member
from library_app.file_handler import read_json, write_json
from library_app.validators import (
    DuplicateRecordError,
    MemberNotFoundError,
    validate_email,
    validate_id,
    validate_text,
)


class MemberService:
    FILE = "members.json"

    def __init__(self):
        self.members = [
            Member.from_dict(item)
            for item in read_json(self.FILE)
        ]

    def _save(self):
        write_json(
            self.FILE,
            [member.to_dict() for member in self.members],
        )

    def register_member(self, member_id, name, email):
        member_id = validate_id(member_id, "Member ID")
        name = validate_text(name, "Name")
        email = validate_email(email)

        if any(
            member.member_id == member_id
            for member in self.members
        ):
            raise DuplicateRecordError(
                f"Member ID {member_id} already exists."
            )

        member = Member(member_id, name, email)
        self.members.append(member)

        try:
            self._save()
        except Exception:
            self.members.remove(member)
            raise

        return member

    def list_members(self):
        return list(self.members)

    def get_member(self, member_id):
        member_id = validate_id(member_id, "Member ID")

        for member in self.members:
            if member.member_id == member_id:
                return member

        raise MemberNotFoundError(
            f"Member ID {member_id} not found."
        )
