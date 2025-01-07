import enum
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional

from sqlmodel import JSON
from sqlmodel import Column
from sqlmodel import Enum
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class PostStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "DRAFT"


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=100)
    content: str = Field(...)
    user_id: int | None = Field(foreign_key="user.id", nullable=True)
    post_date: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False)
    post_modified: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False)
    post_status: PostStatus = Field(sa_column=Column(Enum(PostStatus)), default=PostStatus.DRAFT)
    post_metadata: dict | None = Field(sa_column=Column(JSON), default=None)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="posts")


class PostCreate(SQLModel):
    title: str
    content: str
    post_status: PostStatus | None = PostStatus.DRAFT
    post_metadata: dict | None = None


class PostRead(SQLModel):
    id: int
    title: str
    content: str
    user_id: int | None
    post_status: PostStatus
    post_date: datetime
    post_modified: datetime
    post_metadata: dict | None
