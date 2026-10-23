
import pytest

from library_app.member_service import MemberService
from library_app.validators import DuplicateRecordError


@pytest.fixture
def service(tmp_path, monkeypatch):
    import library_app.file_handler as fh

    monkeypatch.setattr(fh, "DATA_DIR", tmp_path)
    return MemberService()


def test_register_member(service):
    member = service.register_member(
        "M001", "Alex", "alex@example.com"
    )

    assert member.member_id == "M001"
    assert member.name == "Alex"


def test_duplicate_member_rejected(service):
    service.register_member(
        "M001", "Alex", "alex@example.com"
    )

    with pytest.raises(DuplicateRecordError):
        service.register_member(
            "M001", "Sam", "sam@example.com"
        )
