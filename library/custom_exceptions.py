class LibraryError(Exception):
    """Base exception for all library-related errors."""
    pass

class BookAvailabilityError(LibraryError):
    """Raised when a book is not available for borrowing."""
    pass

class UserAuthenticationError(LibraryError):
    """Raised when there are issues with user authentication."""
    pass

class DueDateViolationError(LibraryError):
    """Raised when a book is returned after its due date."""
    pass

class DatabaseConnectionError(LibraryError):
    """Raised when there are database connection issues."""
    pass

class InvalidISBNError(LibraryError):
    """Raised when an ISBN format is invalid."""
    pass

class InvalidEmailError(LibraryError):
    """Raised when an email format is invalid."""
    pass

class InvalidPhoneNumberError(LibraryError):
    """Raised when a phone number format is invalid."""
    pass 