from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import app_config
from app.core.logger import main_logger

DATABASE_URL = app_config.DATABASE_URL  # Fetch the database URL from the application configuration
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

# Create a sessionmaker for producing async database sessions
async_session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Initialize the database by verifying connectivity."""
    try:
        # Check database connectivity
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        main_logger.info("Database connection successful.")
    except Exception as e:
        main_logger.error(f"Failed to initialize the database: {type(e).__name__}: {str(e)}")
        raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for request handling, ensuring proper session lifecycle management.
    Used as a FastAPI dependency to inject a database session into endpoints.
    """
    session = async_session_maker()
    try:
        main_logger.debug("Creating a new database session.")
        yield session
    except Exception as e:
        main_logger.error(f"Error during database session: {type(e).__name__}: {str(e)}")
        raise  # Re-raise the exception, TODO: do we really need to raise it?
    finally:
        await session.close()
        main_logger.debug("Database session closed.")
