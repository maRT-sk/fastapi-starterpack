from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig
from starlette_admin.auth import AdminUser
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.core.auth.backend import verify_user_pw_from_db
from app.core.auth.exeptions import AuthenticationError


class MyAuthProvider(AuthProvider):
    """
    AuthProvider that authenticates against the User table in the database with hashed passwords.
    """

    # TODO: Improve this by using app.core.auth
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        try:
            user = await verify_user_pw_from_db(username, password)
        except AuthenticationError:
            raise LoginFailed("Invalid username or password") from AuthenticationError

        if user.is_superuser:
            request.session.update({"is_superuser": True})
            return response
        else:
            raise LoginFailed("Insufficient privileges to access this resource.")

    # TODO: Improve this by using app.core.auth
    async def is_authenticated(self, request: Request) -> bool:
        return bool(request.session.get("is_superuser"))

    def get_admin_config(self, request: Request) -> AdminConfig:
        # username: str | None = request.session.get("username")
        # custom_app_title = f"Hello {username}!"
        custom_app_title = "Admin Panel"
        return AdminConfig(app_title=custom_app_title)

    def get_admin_user(self, request: Request) -> AdminUser:
        return AdminUser(username="admin")

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
