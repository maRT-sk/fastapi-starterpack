from loguru import logger
from sqlalchemy.future import select
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend

from app.core.auth.models import AuthUser
from app.core.auth.security import pwd_context
from app.core.config import app_config
from app.core.database import get_session
from app.core.utils.exceptions import AuthError
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
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        # Verify the password using the password hashing context
        if not user or not pwd_context.verify(password, user.password):
            raise AuthError.InvalidCredentialsError("Invalid username or password")
        return user  # Return the user object if authentication is successful


class BasicAuthBackend(AuthenticationBackend):
    """
    A basic authentication backend for verifying username and password.

    This implementation supports:
    - 1. Session-based authentication (via the session cookie)
    - 2. Authentication via headers using username and password
    - 3. Special authentication via headers using "SECRET_KEY" as username and SECRET_KEY value as password
    - 4. TODO: Add support for token-based authentication
    """

    async def authenticate(self, conn):
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

        # 2. Authentication via headers using username and password
        # Check for Authorization-Username and Authorization-Password in the headers
        if "Authorization-Username" in conn.headers and "Authorization-Password" in conn.headers:
            auth_username = conn.headers["Authorization-Username"]
            auth_password = conn.headers["Authorization-Password"]

            # 3. Special admin authentication via a secret key
            # If the username and password match the SECRET_KEY environment variable,
            if auth_username == "SECRET_KEY" and auth_password == str(app_config.SECRET_KEY):
                logger.debug("Authenticated via env variable SECRET_KEY.")
                return AuthCredentials(["authenticated", "admin"]), AuthUser(display_name="secret_admin")

            user = await verify_user_pw_from_db(auth_username, auth_password)

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
