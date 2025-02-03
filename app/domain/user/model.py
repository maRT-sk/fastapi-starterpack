from datetime import UTC
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core import Base
from app.domain.permission.model import user_permission_table


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String(50), nullable=False, unique=True)
    email = mapped_column(String(100), nullable=True, unique=True)
    full_name = mapped_column(String(100), nullable=True)
    is_active = mapped_column(Boolean, default=True)
    is_superuser = mapped_column(Boolean, default=False)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(UTC))
    last_login = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    posts = relationship("Post", back_populates="user", lazy="selectin")
    user_permissions = relationship(
        "Permission", secondary=user_permission_table, back_populates="users", lazy="selectin"
    )
