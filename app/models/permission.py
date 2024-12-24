from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from app.models._links import UserPermissionLink

if TYPE_CHECKING:
    from app.models.user import User


class Permission(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100, unique=True)
    description: str | None = Field(default=None, max_length=255)

    # Relationships
    users: list["User"] = Relationship(back_populates="user_permissions", link_model=UserPermissionLink)
