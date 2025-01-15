from datetime import UTC
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.core.auth.security import hash_password
from app.models import Base
from app.models._links import user_permission_table


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC).replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now(UTC).replace(tzinfo=None))
    last_login = Column(DateTime, nullable=True)

    # Relationships
    posts = relationship("Post", back_populates="user", lazy="selectin")
    user_permissions = relationship(
        "Permission", secondary=user_permission_table, back_populates="users", lazy="selectin"
    )


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50, description="Username of the user (max 50 characters)")
    full_name: str | None = Field(None, max_length=100, description="Full name of the user (max 100 characters)")
    password: str = Field(..., min_length=8, description="Password for the user (min 8 characters)")
    is_superuser: bool | None = Field(False, description="Indicates if the user has superuser privileges")

    @field_validator("password")
    @classmethod
    def password_to_hashed_password(cls, v: str) -> str:
        """Hash the password before saving."""
        return hash_password(v)

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    username: str
    email: str | None
    full_name: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None

    class Config:
        from_attributes = True
