import binascii

from loguru import logger
from sqlmodel import select
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.authentication import AuthenticationError

from app.core.auth.models import AuthUser
from app.core.auth.security import pwd_context
from app.core.config import app_config
from app.core.database import get_session  # Use the session generator
from app.models.user import User


async def verify_user_pw_from_db(username: str, password: str) -> User:
    """
    Verify a user's password from the database.

    Args:
        username (str): The username to verify.
        password (str): The password to check against the hashed password in the database.

    Returns:
        User: The authenticated user object.

    Raises:
        AuthenticationError: If the username or password is invalid.
    """

    async for session in get_session():
        # Query the database for a user with the given username
        user = await session.scalar(select(User).where(User.username == username))
        # Verify the password using the password hashing context
        if not user or not pwd_context.verify(password, user.password):
            raise AuthenticationError("Invalid username or password")
        return user  # Return the user object if authentication is successful


class BasicAuthBackend(AuthenticationBackend):
    """
    A basic authentication backend for verifying username and password.

    This implementation supports:
    - 1. Session-based authentication (via the session cookie)
    - 2. Basic Authentication via the Authorization header (via via the Authorization header)
    - 3. Special admin authentication via a secret key from environment variables (via the Authorization header)
    - 4. TODO: Add support for token-based authentication
    """

    async def authenticate(self, conn):  # noqa: PLR0911 TODO
        # 1. Session-based authentication
        # Check if session-based authentication is available
        if conn.session:
            authentificated_user = AuthUser(
                display_name=conn.session.get("username"),
                identity=conn.session.get("identity"),
            )

            if conn.session.get("is_superuser"):
                logger.debug("Authenticated via session with superuser privileges.")
                return AuthCredentials(["authenticated", "admin"]), authentificated_user
            else:
                logger.debug("Authenticated via session without superuser privileges.")
                return AuthCredentials(["authenticated"]), authentificated_user

        # 2. Basic Authentication via the Authorization header
        # Check if Authorization header is present for Basic Authentication
        elif "Authorization" in conn.headers:
            auth = conn.headers["Authorization"]

            try:
                scheme, credentials = auth.split()
                if scheme.lower() != "basic":
                    return None
                username, password = credentials.split(":")

                # 3. Special admin authentication via a secret key from environment variables
                if username == "SECRET_KEY" and password == str(app_config.SECRET_KEY):
                    logger.debug("Authenticated via env variable SECRET_KEY.")
                    return AuthCredentials(["authenticated", "admin"]), AuthUser(display_name="secret_admin")

                user = await verify_user_pw_from_db(username, password)

            except (AuthenticationError, ValueError, UnicodeDecodeError, binascii.Error):
                raise AuthenticationError("Invalid basic auth credentials") from AuthenticationError

            if user.is_superuser:
                logger.debug("Authenticated via Authorization header with superuser privileges.")
                return AuthCredentials(["authenticated", "admin"]), AuthUser(user)
            else:
                logger.debug("Authenticated via Authorization header without superuser privileges.")
                return AuthCredentials(["authenticated"]), AuthUser(user)

        else:
            # No authentication information provided
            logger.debug("User not authenticated.")
            return None
