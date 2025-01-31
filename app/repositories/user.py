from collections.abc import Sequence
from datetime import UTC
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UsernameAlreadyExistsError(HTTPException):
    """Exception raised when trying to create a user with an existing username."""

    def __init__(self, username: str):
        detail = f"Username '{username}' is already taken."
        super().__init__(status_code=400, detail=detail)


class UserRepository:
    """Repository class for handling User database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        """Fetches a user by their username."""
        result = await self.session.execute(select(User).filter_by(username=username))
        return result.scalars().first()

    async def add(self, user: User) -> None:
        """Adds a new user to the database."""
        existing_user = await self.get_by_username(user.username)
        if existing_user:
            raise UsernameAlreadyExistsError(user.username)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

    async def get(self, user_id: int) -> User | None:
        """Fetches a user by ID."""
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()

    async def list(self, limit: int = 10, offset: int = 0) -> Sequence[User]:
        """Lists users with pagination support."""
        result = await self.session.execute(select(User).order_by(User.created_at.desc()).offset(offset).limit(limit))
        return result.scalars().all()

    async def update(self, user: User, **kwargs: Any) -> None:
        """Updates a user's attributes and saves the changes."""
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.updated_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(user)

    async def delete(self, user: User) -> None:
        """Deletes a user from the database."""
        await self.session.delete(user)
        await self.session.commit()
