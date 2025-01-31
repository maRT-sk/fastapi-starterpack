from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from starlette.authentication import requires

from app.core.database import AsyncSession
from app.core.database import get_session
from app.models.post import Post
from app.models.post import PostCreate
from app.models.post import PostRead

router = APIRouter()


@router.post("/", response_model=PostRead)
@requires("admin")
async def create_post(
    request: Request, post_data: PostCreate, session: AsyncSession = Depends(get_session)
) -> PostRead:
    """
    Create a new post in the database.

    Args:
        request (Request): Required by the `@requires` decorator for authorization.
        post_data (PostCreate): The data for creating a new post.
        session (AsyncSession): Database session dependency.

    Returns:
        PostRead: The newly created post in the `PostRead` format.
    """
    post = Post(**post_data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return PostRead.model_validate(post)
