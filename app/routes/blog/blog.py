from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.templates import main_templates
from app.repositories.post import PostRepository
from app.schemas.post import PostSchema

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def blog_page(request: Request, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
    """
    Fetches all blog posts from the database and renders the blog page.
    """
    repository = PostRepository(session)
    posts = await repository.list()
    context = {"request": request, "posts": posts}
    return main_templates.TemplateResponse("blog/blog.html", context)


@router.get("/{post_id}", response_class=HTMLResponse, name="blog")
async def blog_page_single(
    post_id: int, request: Request, session: AsyncSession = Depends(get_session)
) -> HTMLResponse:
    """
    Fetches a single blog post from the database based on the post_id and renders the single blog HTML template.
    """
    repository = PostRepository(session)
    post = await repository.get(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_schema = PostSchema.Read.model_validate(post)

    context = {"request": request, "post": post_schema}
    return main_templates.TemplateResponse("blog/single_blog.html", context)
