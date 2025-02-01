from pydantic import BaseModel
from pydantic import Field


class PermissionSchema(BaseModel):
    class Create(BaseModel):
        name: str = Field(..., max_length=100, description="Name of the permission (max 100 characters)")
        description: str | None = Field(None, max_length=255, description="Optional description of the permission")
