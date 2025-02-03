from enum import Enum


class ErrorResponseType(str, Enum):
    """Enum to represent response formats supported by the application."""

    HTML = "html"
    JSON = "json"
