from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field

from app.models.post import PostStatus


class PostSchema:
    class Create(BaseModel):
        title: str = Field(..., max_length=100, description="Title of the post (max 100 characters)")
        content: str = Field(..., description="Content of the post")
        post_status: PostStatus = Field(PostStatus.DRAFT, description="Status of the post")
        post_metadata: dict[str, Any] | None = Field(None, description="Optional metadata for the post")

        class Config:
            from_attributes = True

    class Read(BaseModel):
        id: int
        title: str
        content: str
        user_id: int | None
        post_status: PostStatus
        post_date: datetime
        post_modified: datetime
        post_metadata: dict[str, Any] | None

        class Config:
            from_attributes = True

    class Delete(BaseModel):
        message: str
