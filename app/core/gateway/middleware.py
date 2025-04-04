from collections.abc import Awaitable
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response

from app.core.gateway.error_response import create_error_response
from app.core.logging import main_logger

# === TYPE ALIASES ===
NextCallable = Callable[[Request], Awaitable[Response]]


# === MIDDLEWARES ===
class BasicCSRFMiddleware(BaseHTTPMiddleware):
    """Middleware to handle Cross-Site Request Forgery (CSRF) protection by checking for a CSRF flag in cookies."""

    # NOTE: Same-site cookies help prevent CSRF attacks, but additional protection is recommended.

    CSRF_COOKIE_NAME = "csrf_flag"  # Name of the cookie
    CSRF_COOKIE_VALUE = "1"  # Value of the cookie
    CSRF_MAX_AGE = 24 * 60 * 60  # Cookie expires in 24 hours

    async def dispatch(self, request: Request, call_next: NextCallable) -> Response | JSONResponse:
        """
        Middleware behavior:
        - For non-GET requests, it verifies the presence of the CSRF flag in cookies.
        - If missing, responds with 403 Forbidden.
        - Adds the CSRF flag to outgoing responses if it was not previously set.
        """
        # Reject non-GET requests if the CSRF flag is not present in the cookies
        if request.method != "GET" and not request.cookies.get("csrf_flag"):
            main_logger.warning(f"CSRF token missing or invalid for {request.method} request to {request.url.path}")
            return create_error_response(request, status_code=403, detail="CSRF flag is missing or invalid.")

        # Store the CSRF flag in the `request.state` object for further use downstream
        request.state.csrf_flag = request.cookies.get("csrf_flag", None)
        response: Response = await call_next(request)  # Pass the request to the next middleware or route handler

        # If the CSRF flag was not previously set, set it on the response
        if not request.state.csrf_flag:
            response.set_cookie(
                key=self.CSRF_COOKIE_NAME,
                value=self.CSRF_COOKIE_VALUE,
                max_age=self.CSRF_MAX_AGE,
                path="/",  # Cookie is valid for the entire domain
                samesite="strict",  # Enforce strict SameSite policy to prevent CSRF attacks
                secure=True,  # Ensure the cookie is only sent over HTTPS
                httponly=True,  # Prevent JavaScript access to the cookie
            )
        return response


class AdvancedCSRFMiddleware(BaseHTTPMiddleware):
    """Middleware for handling advanced CSRF protection in HTTP requests."""

    ...


class HtmxStateMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check if a request is an HTMX request and set `request.state.is_htmx_request` accordingly.
    - If the request contains the header "hx-request" with value "true", it is marked as an HTMX request.
    - Adds `is_htmx_request` (bool) to `request.state` for downstream usage.
    """

    async def dispatch(self, request: Request, call_next: NextCallable) -> Response:
        request.state.is_htmx_request = request.headers.get("hx-request") == "true"
        response = await call_next(request)
        return response
