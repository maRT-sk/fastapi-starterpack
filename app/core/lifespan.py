from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import check_db_ready
from app.core.database import engine
from app.core.logger import main_logger


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown lifecycle."""

    try:
        main_logger.info("Starting application...")
        await check_db_ready()
        yield
    except Exception as e:
        main_logger.error(f"Application startup failed: {type(e).__name__}: {str(e)}")
        # raise  # Not raising an exception here; logging is sufficient for debugging
    finally:
        main_logger.info("Shutting down application...")
        try:
            await engine.dispose()  # Close database connections
            main_logger.info("Database connections closed successfully.")
        except Exception as e:
            main_logger.error(f"Shutdown cleanup failed: {type(e).__name__}: {str(e)}")
