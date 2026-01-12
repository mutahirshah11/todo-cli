class UserAlreadyExistsException(Exception):
    """Exception raised when trying to create a user that already exists."""
    pass


class InvalidCredentialsException(Exception):
    """Exception raised when user provides invalid credentials."""
    pass


class UserNotActiveException(Exception):
    """Exception raised when trying to authenticate an inactive user."""
    pass