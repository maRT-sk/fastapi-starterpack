from fastapi import Request

from app.core.logger import main_logger


def log_caught_exception(level: str | int, message: str, exc: Exception, request: Request) -> None:
    """Utility to log exceptions with consistent formatting."""
    # Additional logic can be implemented here if needed in the future
    main_logger.log(level, f"{message}: {exc} | Path: {request.url.path}")
