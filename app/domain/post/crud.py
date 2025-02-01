from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.repository import Repository
from app.domain.post.model import Post


class PostRepository(Repository[Post]):
    """Repository class for handling Post database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, post: Post) -> None:
        """Adds a new Post to the database and commits the transaction."""
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

    async def get(self, post_id: int) -> Post | None:
        """Retrieves a Post by its ID from the database."""
        result = await self.session.execute(select(Post).filter_by(id=post_id))
        return result.scalars().first()

    async def list(self) -> list[Post]:
        """Returns a list of all Posts from the database."""
        result = await self.session.execute(select(Post))
        return list(result.scalars().all())

    async def delete(self, post: Post) -> None:
        """Deletes a specified Post from the database and commits the transaction."""
        await self.session.delete(post)
        await self.session.commit()
