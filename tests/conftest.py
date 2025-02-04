import sys
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Base
from app.core import main_logger
from app.core.database import import_models_modules
from app.core.database.engine import engine
from app.core.database.session import async_session_maker


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_teardown():
    """Initialize database once before all tests and clear it after the last test."""
    # TODO: Add any global setup logic if needed (e.g., seed test data)
    yield  # Run all tests
    sys.stdout.write("\n")
    main_logger.debug("All tests completed.")


@pytest_asyncio.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Reset database schema before each test and provide a fresh async session."""

    # Ensure all models are imported before running tests
    import_models_modules()

    # Reset the database schema before each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        sys.stdout.write("\n")
        main_logger.debug("Database reset before test.")

    # Provide a fresh session for the test
    async with async_session_maker() as session:
        yield session  # This session is used in the test
        await session.rollback()
