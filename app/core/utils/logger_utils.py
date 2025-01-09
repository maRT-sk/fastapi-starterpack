from fastapi import Request


def prepare_log_message(message: str, exc: Exception, request: Request) -> str:
    """Generate a formatted log message with consistent structure"""
    return f" {message} | Exception: {exc} | Path: {request.url.path}"
