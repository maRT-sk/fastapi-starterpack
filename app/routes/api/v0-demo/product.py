# TODO: better examples / remove this endpoints
from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import Depends
from sqlmodel import select

from app.core.database import AsyncSession
from app.core.database import get_session
from app.models.demo.product import Product
from app.models.demo.product import ProductCreate

router = APIRouter()


@router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, session: AsyncSession = Depends(get_session)) -> Product:
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("/products", response_model=list[Product])
async def get_all_products(session: AsyncSession = Depends(get_session)) -> Sequence[Product]:
    """
    Retrieve all products from the database.
    """
    product = await session.exec(select(Product))
    products_all = product.all()
    return products_all
