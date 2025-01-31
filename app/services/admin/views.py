from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.views import Link

from app.models.permission import Permission
from app.models.permission import PermissionCreate
from app.models.post import Post
from app.models.post import PostCreate
from app.models.user import User
from app.models.user import UserCreate


# TODO: Find a better way to implement this
class UserView(ModelView):
    fields = [
        User.username,  # type: ignore
        User.full_name,  # type: ignore
        User.email,  # type: ignore
        User.password,  # type: ignore
        User.is_active,  # type: ignore
        User.is_superuser,  # type: ignore
    ]
    exclude_fields_from_list = [User.password]  # type: ignore


def attach_admin_views(admin_interface: Admin) -> None:
    """Adds views to the admin interface."""

    # Add custom views to admin panel
    admin_interface.add_view(CustomView(label="Dashboard", icon="fa fa-home", path="/", template_path="dashboard.html"))

    # Add model views to admin panel
    admin_interface.add_view(UserView(User, pydantic_model=UserCreate, icon="fa fa-users"))
    admin_interface.add_view(ModelView(Permission, pydantic_model=PermissionCreate, icon="fa fa-lock"))
    admin_interface.add_view(ModelView(Post, pydantic_model=PostCreate, icon="fa fa-pen-to-square"))

    # Add links to admin panel
    admin_interface.add_view(Link(label="Go to frontend", icon="fa fa-link", url="/"))

    # TODO
    # Validation via pydantic_model does not work; it might be a Starlette Admin bug.
    # Documentation: https://jowilf.github.io/starlette-admin/user-guide/validations/
