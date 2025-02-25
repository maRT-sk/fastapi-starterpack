from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.core.templates import renderer

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request) -> HTMLResponse:
    """
    Home page endpoint that renders an HTML template.
    """
    return renderer.TemplateResponse("pages/home.html", {"request": request, "description": "Home Page"})
