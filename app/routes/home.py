from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.core.templates import main_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """
    Home page endpoint that renders an HTML template.
    """
    return main_templates.TemplateResponse("core/home.html", {"request": request, "title": "Home Page"})
