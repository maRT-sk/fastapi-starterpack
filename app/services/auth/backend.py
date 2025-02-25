from loguru import logger
from sqlalchemy.future import select
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.requests import HTTPConnection

from app.core.config.settings import app_config
from app.core.database.session import get_session
from app.domain.user.exception import AuthError
from app.domain.user.model import User
from app.services.auth.models import AuthUser
from app.services.auth.security import pwd_context


async def verify_user_pw_from_db(username: str, password: str) -> User | None:
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
        if not user or not pwd_context.verify(password, str(user.password)):
            raise AuthError.InvalidCredentialsError("Invalid username or password")
        return user  # Return the user object if authentication is successful

    return None  # Ensure function always returns something


class BasicAuthBackend(AuthenticationBackend):
    """
    A basic authentication backend for verifying username and password.

    This implementation supports:
    - 1. Session-based authentication (via the session cookie)
    - 2. Authentication via headers using username and password
    - 3. Special authentication via headers using "SECRET_KEY" as username and SECRET_KEY value as password
    - 4. TODO: Add support for token-based authentication
    """

    # TODO: Simplify function
    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, AuthUser] | None:  # noqa: PLR0911
        # 1. Session-based authentication
        # Check if session-based authentication is available
        if conn.session:
            authenticated_user = AuthUser(
                display_name=conn.session.get("username"),
                identity=conn.session.get("identity"),
            )

            if conn.session.get("is_superuser"):
                logger.debug("Authenticated via session with superuser privileges.")
                return AuthCredentials(["authenticated", "admin"]), authenticated_user
            else:
                logger.debug("Authenticated via session without superuser privileges.")
                return AuthCredentials(["authenticated"]), authenticated_user

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
            if not user:
                # Invalid username or password
                logger.debug("Invalid username or password.")
                return None

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
