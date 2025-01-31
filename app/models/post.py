import enum
from datetime import UTC
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models import Base


class PostStatus(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class Post(Base):
    __tablename__ = "post"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(100), nullable=False)
    content = mapped_column(String, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    post_date = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False
    )
    post_modified = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC).replace(tzinfo=None), nullable=False
    )
    post_status = mapped_column(Enum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    post_metadata = mapped_column(JSON, default=None)

    # Relationships
    user = relationship("User", back_populates="posts", lazy="selectin")


class PostCreate(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the post (max 100 characters)")
    content: str = Field(..., description="Content of the post")
    post_status: PostStatus = Field(PostStatus.DRAFT, description="Status of the post")
    post_metadata: dict[str, Any] | None = Field(None, description="Optional metadata for the post")


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int | None
    post_status: PostStatus
    post_date: datetime
    post_modified: datetime
    post_metadata: dict[str, Any] | None
