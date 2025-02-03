from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract base class for a generic repository pattern."""

    @abstractmethod
    async def add(self, entity: T) -> None:
        """Adds a new entity to the database and commits the transaction."""
        pass

    @abstractmethod
    async def get(self, entity_id: int) -> T | None:
        """Retrieves an entity by its ID from the database."""
        pass

    @abstractmethod
    async def list(self) -> list[T]:
        """Returns a list of entities from the database."""
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        """Deletes a specified entity from the database and commits the transaction."""
        pass
