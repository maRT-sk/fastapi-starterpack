from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config.settings import app_config


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
