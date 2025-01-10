from starlette.authentication import AuthenticationError
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig
from starlette_admin.auth import AdminUser
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.core.auth.backend import BasicAuthBackend
from app.core.logger import main_logger


class StarletteAdminAuthProvider(AuthProvider):
    """
    Custom AuthProvider for the Starlette Admin Panel that authenticates users
    using BasicAuthBackend and manages session data.
    """

    def __init__(self):
        super().__init__()
        self.basic_auth_backend = BasicAuthBackend()  # Initialize the authentication backend

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        """
        Authenticate the user using BasicAuthBackend and store session data .
        """
        try:
            # Create a new scope with added custom headers
            modified_scope = dict(request.scope)  # Copy the existing scope
            headers = MutableHeaders(request.headers)
            headers["Authorization-Username"] = username  # Add custom username header
            headers["Authorization-Password"] = password  # Add custom password header
            modified_scope["headers"] = headers.raw
            # Create a new Request object with the modified scope
            modified_request = Request(scope=modified_scope, receive=request.receive)

            # Use BasicAuthBackend's `authenticate` method
            auth_credentials, auth_user = await self.basic_auth_backend.authenticate(modified_request)

            if "admin" in auth_credentials.scopes:  # Set session data if the user has admin privileges
                request.session.update(
                    {
                        "is_superuser": True,
                        "username": auth_user.display_name,
                    }
                )
                return response
            else:
                raise LoginFailed("Insufficient privileges to access this resource.")
        except AuthenticationError:
            raise LoginFailed("Invalid username or password") from AuthenticationError
        except Exception as e:
            main_logger.critical("something went wrong", exc_info=e)
            raise LoginFailed("Invalid username or password") from AuthenticationError

    async def is_authenticated(self, request: Request) -> bool:
        """Check if the user is authenticated based on session data."""
        return bool(request.session.get("is_superuser"))

    def get_admin_config(self, request: Request) -> AdminConfig:
        """Retrieve the admin configuration for the panel."""
        # username: str | None = request.session.get("username")
        # custom_app_title = f"Hello {username}!"
        custom_app_title = "Admin Panel"
        return AdminConfig(app_title=custom_app_title)

    def get_admin_user(self, request: Request) -> AdminUser:
        """Retrieve the currently logged-in admin user."""
        # TODO: add logic to correct get_admin_user
        return AdminUser(username="admin")

    async def logout(self, request: Request, response: Response) -> Response:
        """Log out the user by clearing the session data."""
        request.session.clear()
        return response
