from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app.core.utils.logger_utils import log_caught_exception
from app.core.utils.response_utils import render_error_response


async def handle_internal_server_error(request: Request, exc: Exception) -> Response:
    """Handle unexpected internal server errors (HTTP 500)."""
    log_caught_exception("CRITICAL", "Internal server error occurred", exc, request)
    return render_error_response(
        request,
        status_code=500,
        detail="An internal server error occurred. Please try again later.",
    )


async def handle_validation_exceptions(request: Request, exc: Exception) -> Response:
    """Handle Pydantic validation errors (HTTP 400)."""
    if not isinstance(exc, RequestValidationError):  # This should never happen but ensures type safety at runtime
        raise TypeError(f"Unexpected exception type: {type(exc)}. Expected RequestValidationError.") from exc

    log_caught_exception("INFO", "Client error - validation exception", exc, request)
    return render_error_response(
        request,
        status_code=400,
        detail="Invalid input data. Please check your request.",
        context={"error_detail": exc.errors()},
    )


async def handle_http_exceptions(request: Request, exc: Exception) -> Response:
    """Handle HTTP exceptions raised during request processing."""
    if not isinstance(exc, HTTPException):  # This should never happen but ensures type safety at runtime
        raise TypeError(f"Unexpected exception type: {type(exc)}. Expected HTTPException.") from exc

    if 400 <= exc.status_code < 500:  # Client error  # noqa: PLR2004
        log_caught_exception("WARNING", "A client error occurred", exc, request)
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=exc.detail or "A client error occurred.",
        )
    elif 500 <= exc.status_code < 600:  # Server error  # noqa: PLR2004
        log_caught_exception("ERROR", "Server error occurred", exc, request)
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=exc.detail or "A server error occurred.",
        )
    else:  # Unhandled status codes
        log_caught_exception("CRITICAL", "Unhandled status code", exc, request)
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=f"Unhandled status code: {exc.status_code}",
        )
