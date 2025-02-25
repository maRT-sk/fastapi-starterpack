from sqlalchemy.sql import text

from app.core.database.engine import engine
from app.core.logging import main_logger


async def check_db_ready() -> None:
    """Checks if the database is ready for operations. Verifies connectivity using a lightweight."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            _ = result.scalar()
        main_logger.debug("Database connection successfully established.")
    except Exception as e:
        main_logger.error(f"Failed to initialize the database: {type(e).__name__}: {str(e)}")
        raise
