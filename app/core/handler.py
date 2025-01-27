from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app.core.logger import main_logger
from app.core.utils.logger_utils import prepare_log_message
from app.core.utils.response_utils import render_error_response


async def handle_internal_server_error(request: Request, exc: Exception) -> Response:
    """Handle unexpected internal server errors (HTTP 500)."""
    main_logger.critical(prepare_log_message("Internal server error", exc, request))

    from sqlalchemy.exc import OperationalError

    if isinstance(exc, OperationalError):
        error_context = "A database error occurred while processing your request."
    else:
        error_context = f"An unexpected server error occurred. (Error type: {type(exc).__name__})"

    return render_error_response(
        request,
        status_code=500,
        detail=f"Internal server error: {error_context}",
    )


async def handle_validation_exceptions(request: Request, exc: Exception) -> Response:
    """Handle Pydantic validation errors (HTTP 400)."""
    if not isinstance(exc, RequestValidationError):  # This should never happen but ensures type safety at runtime
        raise TypeError(f"Unexpected exception type: {type(exc)}. Expected RequestValidationError.") from exc

    main_logger.info(prepare_log_message("Client error - validation exception", exc, request))
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
        main_logger.warning(prepare_log_message("Client error", exc, request))
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=exc.detail or "A client error occurred.",
        )
    elif 500 <= exc.status_code < 600:  # Server error  # noqa: PLR2004
        main_logger.error(prepare_log_message("Server error", exc, request))
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=exc.detail or "A server error occurred.",
        )
    else:  # Unhandled status codes
        main_logger.critical(prepare_log_message("Unhandled status code", exc, request))
        return render_error_response(
            request,
            status_code=exc.status_code,
            detail=f"Unhandled status code: {exc.status_code}",
        )
