# example models to showcase some functionally; better models will be introduced later
from sqlmodel import Field
from sqlmodel import SQLModel


class CategoryCreate(SQLModel):
    name: str = Field(..., max_length=50)
    description: str = Field(default=None, max_length=255)
    color: str = Field(default=None, max_length=32)


# Database Model
class Category(CategoryCreate, table=True):
    id: int = Field(default=None, primary_key=True)
