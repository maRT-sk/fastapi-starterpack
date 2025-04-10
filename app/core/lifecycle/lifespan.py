from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import check_db_ready
from app.core.database.engine import engine
from app.core.logging import main_logger
from app.core.utils import log_route_details


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown lifecycle."""
    try:
        main_logger.info("Starting application...")
        await check_db_ready()
        main_logger.info("Database is ready.")
        log_route_details(app.routes)  # Log registered routes
        yield  # Application successfully started
    except Exception as e:
        main_logger.critical(f"Application startup failed: {type(e).__name__}: {str(e)}")
        raise
    finally:  # Ensure shutdown logic is executed in all cases
        try:
            main_logger.info("Shutting down application...")
            await engine.dispose()  # Close database connections
            main_logger.info("Database connections closed successfully.")
        except Exception as e:
            main_logger.error(f"Shutdown cleanup failed: {type(e).__name__}: {str(e)}")
