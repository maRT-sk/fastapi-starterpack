from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession  # Importing AsyncSession from sqlmodel

from app.core.config import app_config
from app.core.logger import main_logger

# Create an asynchronous engine for the database
engine = create_async_engine(
    url=app_config.DATABASE_URL,
    echo=False,  # Set to True to log all database queries for debugging
    pool_recycle=1800,  # Refresh (recycle) database connections every 30 minutes to prevent timeouts
    pool_size=15,  # Number of database connections to keep open and ready for use
    max_overflow=5,  # Extra connections allowed temporarily if all pooled connections are busy
    pool_timeout=30,  # Time (in seconds) to wait for a free connection before raising an error
)
# Create an asynchronous session factory
async_session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def check_db_ready() -> None:
    """Checks if the database is ready for operations. Verifies connectivity using a lightweight."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(select(1))
            _ = result.scalar()
        main_logger.info("Database connection successfully established.")
    except Exception as e:
        main_logger.error(f"Failed to initialize the database: {type(e).__name__}: {str(e)}")
        raise RuntimeError("Database initialization failed.") from e


async def get_session() -> AsyncSession:
    """Provides an async database session and ensures proper lifecycle management."""
    async with async_session_maker() as session:
        main_logger.debug("Async database session created.")
        try:
            yield session
        except Exception as e:
            main_logger.error(f"Error during database session: {type(e).__name__}: {str(e)}")
            raise  # Re-raise exceptions for proper error handling, TODO: do we really need to raise it?
        finally:
            main_logger.debug("Async database session closed.")
