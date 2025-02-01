from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from app.domain.user.services.auth.security import hash_password


class UserSchema:
    class Create(BaseModel):
        username: str = Field(..., max_length=50, description="Username of the user (max 50 characters)")
        full_name: str | None = Field(None, max_length=100, description="Full name of the user (max 100 characters)")
        password: str = Field(..., min_length=8, description="Password for the user (min 8 characters)")
        is_superuser: bool = Field(False, description="Indicates if the user has superuser privileges")

        @field_validator("password")
        @classmethod
        def password_to_hashed_password(cls, v: str) -> str:
            """Hash the password before saving."""
            return hash_password(v)

        class Config:
            from_attributes = True

    class Read(BaseModel):
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

    class Delete(BaseModel):
        message: str
