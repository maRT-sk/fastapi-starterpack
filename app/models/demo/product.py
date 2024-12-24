# example models to showcase some functionally; better models will be introduced later
from sqlmodel import Field
from sqlmodel import SQLModel


class ProductCreate(SQLModel):
    name: str = Field(..., max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


# Database Model
class Product(ProductCreate, table=True):
    id: int = Field(default=None, primary_key=True)
