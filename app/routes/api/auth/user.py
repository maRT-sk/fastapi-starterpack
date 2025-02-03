from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import requires

from app.core import get_session
from app.domain.user.crud import UserRepository
from app.domain.user.model import User
from app.domain.user.schema import UserSchema

router = APIRouter()


@router.post("/users", response_model=UserSchema.Read)
@requires(["admin"])
async def create_user(
    request: Request, user_data: UserSchema.Create, session: AsyncSession = Depends(get_session)
) -> UserSchema.Read:
    """
    Create a new user in the database.
    """
    repository = UserRepository(session)
    user = User(**user_data.model_dump())  # Convert Pydantic model to SQLAlchemy model
    await repository.add(user)  # Use repository to add user
    return UserSchema.Read.model_validate(user)


@router.get("/users", response_model=list[UserSchema.Read])
@requires(["admin"])
async def list_users(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> list[UserSchema.Read]:
    """
    Retrieve a paginated list of users.
    """
    repository = UserRepository(session)
    users = await repository.list()  # Use repository list method
    return [UserSchema.Read.model_validate(user) for user in users]


@router.get("/users/{user_id}", response_model=UserSchema.Read)
@requires(["admin"])
async def get_user(request: Request, user_id: int, session: AsyncSession = Depends(get_session)) -> UserSchema.Read:
    """
    Retrieve a single user by ID.
    """
    repository = UserRepository(session)
    user = await repository.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema.Read.model_validate(user)


@router.delete("/users/{user_id}", response_model=UserSchema.Delete)
@requires(["admin"])
async def delete_user(
    request: Request, user_id: int, session: AsyncSession = Depends(get_session)
) -> UserSchema.Delete:
    """
    Delete a user by ID.
    """
    repository = UserRepository(session)
    user = await repository.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await repository.delete(user)
    return UserSchema.Delete(message=f"User with ID {user_id} deleted successfully")
