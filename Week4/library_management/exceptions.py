"""Custom exceptions used by the library management system."""


class LibraryError(Exception):
    """Base exception for library-related errors."""


class NotFoundError(LibraryError):
    """Raised when a requested book, member, or issue does not exist."""


class ValidationError(LibraryError):
    """Raised when input data is invalid."""


class AvailabilityError(LibraryError):
    """Raised when a book cannot be issued or returned as requested."""
