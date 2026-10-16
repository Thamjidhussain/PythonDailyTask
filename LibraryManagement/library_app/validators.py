
import re


class LibraryError(Exception):
    """Base exception for library application errors."""


class BookNotFoundError(LibraryError):
    """Book does not exist."""


class MemberNotFoundError(LibraryError):
    """Member does not exist."""


class BookUnavailableError(LibraryError):
    """No copies of a book are available."""


class DuplicateRecordError(LibraryError):
    """A record with the same ID already exists."""


class ValidationError(LibraryError):
    """Input data is invalid."""


class DataFileError(LibraryError):
    """A data file cannot be read or written."""


def validate_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_id(value, field_name):
    value = validate_text(value, field_name)

    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValidationError(
            f"{field_name} may contain only letters, numbers, "
            "underscores, and hyphens."
        )

    return value


def validate_quantity(quantity):
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValidationError("Quantity must be an integer.")

    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    return quantity


def validate_email(email):
    email = validate_text(email, "Email")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValidationError("Enter a valid email address.")

    return email
