from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_db
from app.models.product import Product
from app.models.product import ProductCreate

router = APIRouter()


@router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, session: AsyncSession = Depends(get_db)) -> Product:
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("/products", response_model=list[Product])
async def get_all_products(session: AsyncSession = Depends(get_db)) -> Sequence[Product]:
    """
    Retrieve all products from the database.
    """
    result = await session.execute(select(Product))  # Query to select all products
    products = result.scalars().all()  # Retrieve all records as a list of Product objects
    return products
