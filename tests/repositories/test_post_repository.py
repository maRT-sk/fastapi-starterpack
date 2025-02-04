import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.post.crud import PostRepository
from app.domain.post.model import Post


@pytest.mark.asyncio
async def test_add_post(test_db_session: AsyncSession):
    """Test adding and retrieving a post."""
    repository = PostRepository(test_db_session)

    # Add a test post
    new_post = Post(id=1, title="Test Post", content="This is a test post.")
    await repository.add(new_post)

    # Retrieve the post
    retrieved_post = await repository.get(1)

    # Assertions to verify the post is correctly stored
    assert retrieved_post is not None
    assert retrieved_post.id == 1
    assert retrieved_post.title == "Test Post"
    assert retrieved_post.content == "This is a test post."


async def test_get_post(test_db_session: AsyncSession):
    """Test retrieving a post by ID."""
    repository = PostRepository(test_db_session)
    new_post = Post(title="Find Me", content="Test Content")
    await repository.add(new_post)

    fetched = await repository.get(new_post.id)

    assert fetched is not None
    assert fetched.title == "Find Me"


async def test_list_posts(test_db_session: AsyncSession):
    """Test retrieving multiple posts from the database."""
    repository = PostRepository(test_db_session)

    post1 = Post(title="Post 1", content="Content 1")
    post2 = Post(title="Post 2", content="Content 2")

    await repository.add(post1)
    await repository.add(post2)

    posts = await repository.list()

    assert len(posts) == 2  # NOQA: PLR2004
    assert posts[0].title == "Post 1"
    assert posts[1].title == "Post 2"


async def test_delete_post(test_db_session: AsyncSession):
    """Test deleting a post from the database."""
    repository = PostRepository(test_db_session)

    post = Post(title="Delete Me", content="Will be deleted")
    await repository.add(post)

    retrieved_post = await repository.get(1)
    assert retrieved_post.title == "Delete Me"

    await repository.delete(post)

    deleted = await repository.get(post.id)
    assert deleted is None
