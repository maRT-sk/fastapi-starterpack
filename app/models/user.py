from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import model_validator
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from app.models._links import UserPermissionLink
from app.models.permission import Permission
from app.services.user.crypt import hash_password

if TYPE_CHECKING:
    from app.models.permission import Permission


class UserBase(SQLModel):
    username: str = Field(..., max_length=50)
    email: str | None = Field(default=None, max_length=100)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(..., max_length=128)
    hashed_password: str | None = None

    @model_validator(mode="after")
    def hash_password_if_needed(self):
        self.hashed_password = hash_password(self.password)
        return self


class UserRead(UserBase):
    id: int
    created_at: datetime


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False)
    updated_at: datetime | None = Field(default=None)
    last_login: datetime | None = Field(default=None)

    # Relationships
    user_permissions: list["Permission"] = Relationship(back_populates="users", link_model=UserPermissionLink)
