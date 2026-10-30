"""Input validation helpers."""
from datetime import date
from exceptions import ValidationError


def require_text(value: str, field_name: str) -> str:
    """Return trimmed text or raise ValidationError when it is empty."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return value.strip()


def require_positive_int(value: int, field_name: str) -> int:
    """Validate that a value is a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field_name} must be a positive integer.")
    return value


def parse_date(value: str) -> date:
    """Parse an ISO date (YYYY-MM-DD)."""
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Date must use YYYY-MM-DD format.") from exc
