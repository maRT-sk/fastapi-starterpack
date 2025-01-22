from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from app.models.permission import Permission
from app.models.permission import PermissionCreate
from app.models.post import Post
from app.models.post import PostCreate
from app.models.user import User
from app.models.user import UserCreate


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


def attach_admin_views(admin_interface) -> None:
    admin_interface.add_view(UserView(User, pydantic_model=UserCreate))
    admin_interface.add_view(ModelView(Permission, pydantic_model=PermissionCreate))
    admin_interface.add_view(ModelView(Post, pydantic_model=PostCreate))

    # TODO
    # Validation via pydantic_model does not work; it might be a Starlette Admin bug.
    # Documentation: https://jowilf.github.io/starlette-admin/user-guide/validations/
