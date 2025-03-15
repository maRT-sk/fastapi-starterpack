import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator
from collections.abc import Generator
from typing import Any

import pytest
import pytest_asyncio

from app.core.database import Base
from app.core.database import import_models_modules
from app.core.database.engine import engine
from app.core.database.session import async_session_maker


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """Ensure a consistent event loop across all tests to prevent mismatches."""
    loop = asyncio.get_event_loop()
    yield loop  # Provide event loop to pytest
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[Any, Any]:
    """Reset database schema before each test and provide a fresh async session."""

    # Ensure all models are imported before running tests
    import_models_modules()

    # Reset the database schema before each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create a new async session for the test
    async with async_session_maker() as session:
        yield session  # Provide this session to the test function

    # Drop all tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Dispose the engine to close database connections
    await engine.dispose()
