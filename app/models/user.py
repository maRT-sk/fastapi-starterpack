from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from app.core.auth.security import hash_password
from app.models._links import UserPermissionLink
from app.models.post import Post

if TYPE_CHECKING:
    from app.models.permission import Permission


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=50)
    email: str | None = Field(default=None, max_length=100)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    password: str = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False)
    updated_at: datetime | None = Field(default=None)
    last_login: datetime | None = Field(default=None)

    # Relationships
    user_permissions: list["Permission"] = Relationship(back_populates="users", link_model=UserPermissionLink)
    posts: list["Post"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    username: str
    full_name: str | None
    password: str
    is_superuser: bool

    @field_validator("password")
    @classmethod
    def password_to_hashed_password(cls, v: str) -> str:
        """Hash the password before saving."""
        return hash_password(v)


class UserRead(SQLModel):
    id: int
    username: str
    email: str | None
    full_name: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None
