from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database.engine import engine
from app.core.logging import main_logger

# Create an async session factory
async_session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


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
