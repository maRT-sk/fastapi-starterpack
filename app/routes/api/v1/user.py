from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import Depends
from sqlmodel import select

from app.core.database import AsyncSession
from app.core.database import get_session
from app.models.user import User
from app.models.user import UserCreate
from app.models.user import UserRead

router = APIRouter()


# TODO: Implement proper security mechanisms for this endpoint.
@router.post("/users", response_model=UserRead)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    """
    Create a new user in the database.
    """
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# TODO: Implement proper security mechanisms for this endpoint.
@router.get("/users", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(get_session)) -> Sequence[UserRead]:
    """Retrieve a list of all users from the database."""
    result = await session.exec(select(User))
    all_users = result.all()
    return all_users
