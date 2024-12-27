from sqlmodel import Field
from sqlmodel import SQLModel


class ProductFields:
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductCreate(SQLModel):
    id: int = ProductFields.id
    name: str = ProductFields.name
    price: float = ProductFields.price
    quantity: int = ProductFields.quantity


class Product(SQLModel, table=True):
    id: int = ProductFields.id
    name: str = ProductFields.name
    price: float = ProductFields.price
    quantity: int = ProductFields.quantity
