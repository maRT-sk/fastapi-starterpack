from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.core.templates import main_templates
from app.models.post import Post

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def blog_page(request: Request, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
    """
    Fetches all products from the database and renders the partial product table HTML template.
    """
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    context = {"request": request, "posts": posts}
    return main_templates.TemplateResponse("blog/blog.html", context)


@router.get("/{post_id}", response_class=HTMLResponse,  name="blog")
async def blog_page_single(
    post_id: int, request: Request, session: AsyncSession = Depends(get_session)
) -> HTMLResponse:
    """
    Fetches a single blog post from the database based on the post_id and renders the single blog HTML template.
    """
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    context = {"request": request, "post": post}
    return main_templates.TemplateResponse("blog/single_blog.html", context)
