import binascii

from loguru import logger
from sqlmodel import select
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.authentication import AuthenticationError

from app.core.auth.crypt import pwd_context
from app.core.auth.models import AuthUser
from app.core.config import app_config
from app.core.database import get_session  # Use the session generator
from app.models.user import User


async def verify_user_pw_from_db(username: str, password: str) -> User:
    """Verify a user's password from the database."""

    async for session in get_session():
        user = await session.scalar(select(User).where(User.username == username))
        if not user or not pwd_context.verify(password, user.password):
            raise AuthenticationError("Invalid username or password")
        return user


class BasicAuthBackend(AuthenticationBackend):
    """
    A basic authentication backend for verifying username and password.
    """

    async def authenticate(self, conn):  # noqa: PLR0911 TODO
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

        elif "Authorization" in conn.headers:
            auth = conn.headers["Authorization"]

            try:
                scheme, credentials = auth.split()
                if scheme.lower() != "basic":
                    return None
                username, password = credentials.split(":")

                if username == "SECRET_KEY" and password == str(app_config.SECRET_KEY):
                    logger.debug("Authenticated via env variable SECRET_KEY.")
                    return AuthCredentials(["authenticated", "admin"]), AuthUser(display_name="secret_admin")

                user = await verify_user_pw_from_db(username, password)

            except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
                raise AuthenticationError("Invalid basic auth credentials") from exc

            if user.is_superuser:
                logger.debug("Authenticated via Authorization header with superuser privileges.")
                return AuthCredentials(["authenticated", "admin"]), AuthUser(user)
            else:
                logger.debug("Authenticated via Authorization header without superuser privileges.")
                return AuthCredentials(["authenticated"]), AuthUser(user)

        else:
            logger.debug("User not authenticated.")
            return None
