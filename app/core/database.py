from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.core.config import app_config
from app.core.logger import main_logger


class DatabaseEngineFactory:
    """Factory to create a database engine with appropriate settings based on the database type."""

    @staticmethod
    def get_engine(database_url: str) -> AsyncEngine:
        """Creates and returns an asynchronous database engine based on the database URL."""
        if database_url.startswith("sqlite"):
            return DatabaseEngineFactory._create_sqlite_engine()
        elif database_url.startswith("postgres"):
            return DatabaseEngineFactory._create_postgres_engine()
        else:
            raise NotImplementedError(f"Unsupported database URL: {database_url}")

    @staticmethod
    def _create_sqlite_engine() -> AsyncEngine:
        """Create an SQLite database engine."""
        return create_async_engine(
            url=app_config.DATABASE_URL,
            echo=app_config.DB_ECHO,  # Configurable SQL logging
            connect_args={"check_same_thread": False},  # Required for async SQLite
        )

    @staticmethod
    def _create_postgres_engine() -> AsyncEngine:
        """Create a PostgreSQL database engine with connection pooling."""
        return create_async_engine(
            url=app_config.DATABASE_URL,
            echo=app_config.DB_ECHO,  # Configurable SQL logging
            pool_recycle=1800,  # Recycle connections every 30 minutes
            pool_size=15,  # Number of connections to keep open
            max_overflow=5,  # Allow 5 additional temporary connections
            pool_timeout=30,  # Wait up to 30 seconds for a connection
        )


# Create the engine dynamically based on the database URL
engine = DatabaseEngineFactory.get_engine(app_config.DATABASE_URL)

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
            result = await conn.execute(text("SELECT 1"))
            _ = result.scalar()
        main_logger.debug("Database connection successfully established.")
    except Exception as e:
        main_logger.error(f"Failed to initialize the database: {type(e).__name__}: {str(e)}")
        raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
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


Base = declarative_base(cls=AsyncAttrs)


__all__ = ["Base", "AsyncSession", "get_session", "async_session_maker", "engine", "check_db_ready"]
