from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_db
from app.core.templates import main_templates
from app.models.product import Product

router = APIRouter()


@router.get("/products", response_class=HTMLResponse)
async def products(request: Request) -> HTMLResponse:
    """
    Home page endpoint that renders main products demo page.
    """
    return main_templates.TemplateResponse("examples/products.html", {"request": request})


@router.get("/products/partial/product_table", response_class=HTMLResponse)
async def product_table(request: Request, session: AsyncSession = Depends(get_db)) -> HTMLResponse:
    """
    Fetches all products from the database and renders the partial product table HTML template.
    """
    result = await session.execute(select(Product))
    products = result.scalars().all()
    context = {"products": products}
    return main_templates.TemplateResponse("examples/partials/product_table.html", {"request": request, **context})
