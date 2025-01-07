from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.datastructures import Headers
from starlette.responses import Response

from app.core.templates import main_templates


def is_json_response(headers: Headers) -> bool:
    """Utility to determine if a response should be JSON or HTML."""
    # Additional logic can be implemented here if needed in the future
    content_type = headers.get("Content-Type", "").strip().lower()
    # return content_type.startswith("application/json")
    # TODO: For now, we return only JSON responses.
    return True


def render_error_response(
    request: Request,
    status_code: int,
    detail: str,
    context: dict[str, Any] | None = None,
    template: str = "core/error.html",
) -> Response:
    """Utility to create JSON or HTML responses based on the request's content type."""
    if is_json_response(request.headers):
        return JSONResponse(
            status_code=status_code, content={"status_code": status_code, "detail": detail, "context": context}
        )
    else:
        context = context or {}
        context.update({"request": request, "status_code": status_code, "status_detail": detail})
        return main_templates.TemplateResponse(template, context, status_code=status_code)
