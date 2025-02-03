from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.datastructures import Headers
from starlette.responses import Response

from app.core.data.enums import ErrorResponseType
from app.core.rendering.templates import main_templates

# Default content type used when no valid Content-Type header is provided.
# Consider moving this to the application settings in future versions to allow easier configuration.
DEFAULT_ERROR_RESPONSE_TYPE = ErrorResponseType.HTML


def decide_error_response_type(headers: Headers) -> ErrorResponseType:
    """Utility to determine if a response should be JSON or HTML."""
    client_content_type = headers.get("Content-Type", "").strip().lower()

    if "json" in client_content_type:
        return ErrorResponseType.JSON
    elif "html" in client_content_type:
        return ErrorResponseType.HTML
    else:
        return DEFAULT_ERROR_RESPONSE_TYPE


def create_error_response(
    request: Request,
    status_code: int,
    detail: str,
    context: dict[str, Any] | None = None,
    template: str = "core/error.html",
) -> Response:
    """
    Utility to create JSON or HTML responses based on the request's content type.

    Args:
        request (Request): The FastAPI request object.
        status_code (int): The HTTP status code for the response.
        detail (str): A human-readable message describing the error.
        context (Optional[dict[str, Any]]): Additional context for the response or template.
        template (str): The template to use for HTML responses.

    Returns:
        Response: A JSON or HTML response based on the `Content-Type` header.
    """
    response_type: ErrorResponseType = decide_error_response_type(request.headers)

    if response_type == ErrorResponseType.JSON:
        return JSONResponse(
            status_code=status_code,
            content={"status_code": status_code, "detail": detail},
        )
    elif response_type == ErrorResponseType.HTML:
        context = context or {}
        context.update({"request": request, "status_code": status_code, "status_detail": detail})
        return main_templates.TemplateResponse(template, context, status_code=status_code)
    else:
        # This should never happen, but ensures safety
        raise ValueError(f"Unhandled response type: {response_type}")


def prepare_log_message(message: str, exc: Exception, request: Request) -> str:
    """Generate a formatted log message with consistent structure"""
    error_name = type(exc).__name__
    error_message = str(exc)
    return f" {message} | Path: {request.url.path} | {error_name}: {error_message}"
