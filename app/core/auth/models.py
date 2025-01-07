from starlette.authentication import BaseUser

from app.models.user import User


class AuthUser(BaseUser):
    def __init__(self, user: User | None = None, display_name: str | None = None, identity: str | None = None):
        """
        Initialize an AuthenticatedUser instance.

        Args:
            user: An instance of the User model or None.
            display_name: A custom display name for the user, optional.
            identity: A custom identifier for the user, optional.
        """
        self._user = user
        self._display_name = display_name or (user.username if user else "")
        self._identity = identity or (str(user.id) if user else "")

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        """Returns the display name of the user."""
        return self._display_name

    @property
    def identity(self) -> str:
        """Returns the unique identifier of the user."""
        return self._identity

    @property
    def user(self) -> User | None:
        """Returns the User instance associated with this AuthenticatedUser."""
        return self._user
