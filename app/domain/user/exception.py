from fastapi import HTTPException


class UsernameAlreadyExistsError(HTTPException):
    """Exception raised when trying to create a user with an existing username."""

    def __init__(self, username: str):
        detail = f"Username '{username}' is already taken."
        super().__init__(status_code=400, detail=detail)
