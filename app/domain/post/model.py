from datetime import UTC
from datetime import datetime

from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.domain.post.enums import PostStatus


class Post(Base):
    __tablename__ = "post"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(100), nullable=False)
    content = mapped_column(String, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    post_date = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    post_modified = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    post_status = mapped_column(Enum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    post_metadata = mapped_column(JSON, default=None)

    # Relationships
    user = relationship("User", back_populates="posts", lazy="selectin")

    def publish(self) -> None:
        """Publishes the post by setting its status and updating the modified timestamp."""
        self.post_status = PostStatus.PUBLISHED
        self.post_modified = datetime.now(UTC)
