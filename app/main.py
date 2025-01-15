from fastapi import FastAPI

from app.core.config import app_config
from app.core.database import engine
from app.core.lifespan import app_lifespan
from app.core.logger import setup_logging
from app.core.utils.toml_utils import get_version_from_pyproject
from app.services.admin.provider import StarletteAdminAuthProvider
from app.services.admin.views import attach_admin_views


class AppManager:
    """
    Manages the initialization and configuration of a FastAPI application.

    Responsibilities:
    - Middleware setup
    - Exception handling
    - Static file mounting
    - Route loading
    - Documentation configuration
    - Feel free to add your own
    """

    def __init__(self, app: FastAPI) -> None:
        """
        Initialize the AppManager with a FastAPI instance.

        Args:
            app (FastAPI): The FastAPI application instance to be managed.
        """
        self.app: FastAPI = app
        self.is_production: bool = not app_config.DEBUG
        self.setup_application()

    def setup_application(self) -> None:
        """Apply all configurations to the FastAPI application."""
        self.setup_middlewares()
        self.register_exception_handlers()
        self.mount_static_files()
        self.load_routes()
        self.setup_admin_interface()

    def setup_middlewares(self) -> None:
        """Configures middleware for the FastAPI application."""
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
        from starlette.middleware.authentication import AuthenticationMiddleware
        from starlette.middleware.gzip import GZipMiddleware
        from starlette.middleware.sessions import SessionMiddleware
        from starlette.middleware.trustedhost import TrustedHostMiddleware

        from app.core.auth.backend import BasicAuthBackend
        from app.core.middleware import CSRFMiddleware

        # Add common middleware
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)
        self.app.add_middleware(
            AuthenticationMiddleware,
            backend=BasicAuthBackend(),
            # TODO , on_error=on_auth_error
        )
        self.app.add_middleware(SessionMiddleware, secret_key=app_config.SECRET_KEY)

        # Add production-specific middleware
        if self.is_production:
            self.app.add_middleware(CSRFMiddleware)
            self.app.add_middleware(TrustedHostMiddleware, allowed_hosts=app_config.ALLOWED_HOSTS)
            self.app.add_middleware(HTTPSRedirectMiddleware)
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

    def register_exception_handlers(self) -> None:
        """Register custom exception handlers for the application."""
        from fastapi.exceptions import RequestValidationError
        from starlette.exceptions import HTTPException  # NOTE: Use HTTPException from starlette

        from app.core.handler import handle_http_exceptions
        from app.core.handler import handle_internal_server_error
        from app.core.handler import handle_validation_exceptions

        self.app.add_exception_handler(RequestValidationError, handle_validation_exceptions)
        self.app.add_exception_handler(HTTPException, handle_http_exceptions)
        self.app.add_exception_handler(Exception, handle_internal_server_error)

    def disable_documentation(self) -> None:
        """Disables API documentation if in production."""
        if self.is_production:
            self.app.docs_url = None
            self.app.redoc_url = None
            self.app.openapi_url = None

    def mount_static_files(self) -> None:
        """Mount the static files directory to serve static assets."""
        from fastapi.staticfiles import StaticFiles

        self.app.mount("/static", StaticFiles(directory="app/static"), name="static")

    def setup_admin_interface(self) -> None:
        """Sets up the admin interface."""

        # from starlette.middleware.sessions import SessionMiddleware
        from starlette.middleware import Middleware
        from starlette.middleware.sessions import SessionMiddleware
        from starlette_admin.contrib.sqla import Admin

        admin_interface: Admin = Admin(
            engine,
            title="Example: Auth",
            base_url="/admin",
            statics_dir="app/static",
            login_logo_url="/admin/statics/logo.svg",
            auth_provider=StarletteAdminAuthProvider(),
            middlewares=[
                Middleware(SessionMiddleware, secret_key=app_config.SECRET_KEY),
            ],
            templates_dir="app/templates/admin",
            debug=app_config.DEBUG,
        )

        attach_admin_views(admin_interface)
        admin_interface.mount_to(self.app)

    def load_routes(self) -> None:
        """Load and register all application routes."""
        from app.routes import main_router

        # All routes from the `routes` folder are gathered automatically within main_router
        app.include_router(main_router)


# Setup application logging
setup_logging()

# Create FastAPI application instance
app = FastAPI(
    title="Product Management API",
    version=get_version_from_pyproject(),
    lifespan=app_lifespan,
)

# Initialize and configure the application using AppManager
AppManager(app)
