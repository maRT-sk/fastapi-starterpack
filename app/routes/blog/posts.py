from fastapi import APIRouter
from fastapi import Depends

from app.core.database import AsyncSession
from app.core.database import get_session
from app.models.post import Post
from app.models.post import PostCreate
from app.models.post import PostRead

router = APIRouter()


@router.post("/", response_model=PostRead)
async def create_post(post_data: PostCreate, session: AsyncSession = Depends(get_session)) -> PostRead:
    """
    Create a new user in the database.
    """
    post = Post(**post_data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
