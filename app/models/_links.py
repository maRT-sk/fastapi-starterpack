from sqlmodel import Field
from sqlmodel import SQLModel


class UserPermissionLink(SQLModel, table=True):
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
