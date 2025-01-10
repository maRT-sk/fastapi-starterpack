# # TODO: REMOVE THIS FILE
#
# from fastapi import APIRouter
# from fastapi import Depends
# from fastapi import Request
# from fastapi.responses import HTMLResponse
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.core.database import get_session
# from app.core.templates import main_templates
#
# router = APIRouter()
#
#
# @router.get("/", response_class=HTMLResponse)
# async def products(request: Request) -> HTMLResponse:
#     """
#     Home page endpoint that renders main products demo page.
#     """
#     return main_templates.TemplateResponse("demo/products/products.html", {"request": request})
#
#
# @router.get("/partial/product_table", response_class=HTMLResponse)
# async def product_table(request: Request, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
#     """
#     Fetches all products from the database and renders the partial product table HTML template.
#     """
#     # result = await session.execute(select(Product))
#     # products = result.scalars().all()
#     context = {"products": "a"}
#     return main_templates.TemplateResponse("demo/products/partials/product_table.html", {"request": request, **context})
