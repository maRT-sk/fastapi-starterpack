from fastapi import HTTPException


class AuthError:
    """A container for our auth exceptions used in the application."""

    class InvalidCredentialsError(Exception):
        """Exception raised for invalid username or password."""

        pass

    # TODO: add more and use them
    class UserNotFoundError(Exception):
        """Exception raised when a user cannot be found in the database."""

        pass

    class PermissionDeniedError(Exception):
        """Exception raised when a user does not have sufficient permissions."""

        pass

    class TokenExpiredError(Exception):
        """Exception raised when an authentication token has expired."""

        pass


class UsernameAlreadyExistsError(HTTPException):
    """Exception raised when trying to create a user with an existing username."""

    def __init__(self, username: str):
        detail = f"Username '{username}' is already taken."
        super().__init__(status_code=400, detail=detail)
