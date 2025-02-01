from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import requires

from app.core.database import get_session
from app.domain.post.crud import PostRepository
from app.domain.post.model import Post
from app.domain.post.schema import PostSchema

router = APIRouter()


@router.post("/", response_model=PostSchema.Read)
@requires(["admin"])
async def create_post(
    request: Request, post_data: PostSchema.Create, session: AsyncSession = Depends(get_session)
) -> PostSchema.Read:
    """
    Create a new post in the database.

    Args:
        request (Request): Required by the `@requires` decorator for authorization.
        post_data (PostCreate): The data for creating a new post.
        session (AsyncSession): Database session dependency.

    Returns:
        PostRead: The newly created post in the `PostRead` format.
    """
    repository = PostRepository(session)
    post = Post(**post_data.model_dump(exclude_none=True))  # Convert Pydantic model to SQLAlchemy model
    await repository.add(post)
    return PostSchema.Read.model_validate(post)


@router.delete("/{post_id}", response_model=PostSchema.Delete)
@requires(["admin"])
async def delete_post(
    post_id: int, request: Request, session: AsyncSession = Depends(get_session)
) -> PostSchema.Delete:
    """
    Deletes a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.
        request (Request): Required by the `@requires` decorator for authorization.
        session (AsyncSession): Database session dependency.

    Returns:
        PostSchema.Delete: A confirmation message.
    """
    repository = PostRepository(session)
    post = await repository.get(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await repository.delete(post)

    return PostSchema.Delete(message=f"Post with ID {post_id} deleted successfully")
