from fastapi import Request


def prepare_log_message(message: str, exc: Exception, request: Request) -> str:
    """Generate a formatted log message with consistent structure"""
    error_name = type(exc).__name__
    error_message = str(exc)
    return f" {message} | Path: {request.url.path} | {error_name}: {error_message}"
