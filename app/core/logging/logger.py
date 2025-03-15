import inspect
import logging
import sys

from loguru import logger

from app.core.config.settings import app_config


def configure_loguru() -> None:
    """Configure Loguru's logger to handle both console and file logging."""
    logger.remove()

    # Log to stdout (console)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        level=app_config.LOG_LEVEL,
        colorize=True,
    )

    # Log to a file
    logger.add(
        app_config.LOG_FILE,  # Path to the log file
        rotation="00:00",  # New file is created each day at 00:00
        # rotation="10 MB",  # Automatically rotate the file when it exceeds 10 MB
        retention="7 days",  # Keep log files for 7 days before deleting them
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        compression="zip",  # Compress old log files to save space
        level=app_config.LOG_LEVEL,
    )


class InterceptHandler(logging.Handler):
    """A handler that routes Python's standard logging messages to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log message by forwarding it to Loguru.
        This implementation is based on the Loguru documentation on integrating
        Loguru with the standard logging module. For details, refer to:
        https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
        """
        try:
            level: str | int = logger.level(record.levelname).name  # Map standard logging level to Loguru level
        except ValueError:
            level = record.levelno  # Fallback for unknown levels

        # Find the caller’s frame to preserve accurate logging context
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        # Log the message with depth and exception info if any
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """Sets up application-wide logging configuration using Loguru."""
    configure_loguru()

    # Redirect standard logging to Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logging.root.handlers = [InterceptHandler()]  # Replace existing root handlers with the custom handler
    logger.info("Loguru configured and handling all logs.")

    # Update all existing loggers in the application to use Loguru
    for name in logging.root.manager.loggerDict:
        logger_obj = logging.getLogger(name)
        logger_obj.handlers = [InterceptHandler()]
        logger_obj.propagate = False


def get_logger(name: str):  # type: ignore
    """Returns a Loguru logger instance bound to the specified module or component."""
    return logger.bind(module=name)
