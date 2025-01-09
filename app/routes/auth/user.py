from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from sqlmodel import select
from starlette.authentication import requires

from app.core.database import AsyncSession
from app.core.database import get_session
from app.models.user import User
from app.models.user import UserCreate
from app.models.user import UserRead

router = APIRouter()


@router.post("/users", response_model=UserRead)
@requires("admin")
async def create_user(
    request: Request, user_data: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    """
    Create a new user in the database.

    Args:
        request (Request): Required by the `@requires` decorator for authorization.
        user_data (UserCreate): The data for creating a new user.
        session (AsyncSession): Database session dependency.

    Returns:
        UserRead: The newly created user in the `UserRead` format.
    """
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/users", response_model=list[UserRead])
@requires("admin")
async def list_users(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> Sequence[UserRead]:
    """
    Retrieve a list of all users from the database.

    Args:
        request (Request): Required by the `@requires` decorator for authorization.
        session (AsyncSession): Database session dependency.

    Returns:
        Sequence[UserRead]: A list of user details in the `UserRead` format.
    """
    result = await session.exec(select(User))
    all_users = result.all()

    # Convert User instances to UserRead instances using `model_dump`
    user_reads = [UserRead(**user.model_dump()) for user in all_users]
    return user_reads
