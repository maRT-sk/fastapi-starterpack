from sqlmodel import select
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig
from starlette_admin.auth import AdminUser
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import FormValidationError
from starlette_admin.exceptions import LoginFailed

from app.core.database import async_session_maker
from app.models.user import User
from app.services.admin.crypt import verify_password


class MyAuthProvider(AuthProvider):
    """
    AuthProvider that authenticates against the User table in the database with hashed passwords.
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        async with async_session_maker() as session:
            user = await session.exec(select(User).where(User.username == username))
            user = user.first()

            if not user:
                raise FormValidationError({"username": "User does not exist or is not an admin"})

            if not verify_password(password, user.password):
                raise LoginFailed("Invalid username or password")

            request.session.update({"username": user.username})
            return response

    async def is_authenticated(self, request: Request) -> bool:
        return bool(request.session.get("username"))

    def get_admin_config(self, request: Request) -> AdminConfig:
        username: str | None = request.session.get("username")
        custom_app_title = f"Hello {username}!"
        return AdminConfig(app_title=custom_app_title)

    def get_admin_user(self, request: Request) -> AdminUser:
        return AdminUser(username="admin")

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
