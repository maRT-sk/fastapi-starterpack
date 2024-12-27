from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.contrib.sqlmodel import Admin

from app.models.demo.product import Product
from app.models.demo.product import ProductCreate
from app.models.permission import Permission
from app.models.user import User
from app.models.user import UserCreate

# from starlette_admin.contrib.sqlmodel import ModelView


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
    admin_interface.add_view(UserView(User, pydantic_model=UserCreate))
    admin_interface.add_view(ModelView(Permission, pydantic_model=Permission))
    admin_interface.add_view(ModelView(Product, pydantic_model=ProductCreate))

    # TODO
    # Validation via pydantic_model does not work; it might be a Starlette Admin bug.
    # Documentation: https://jowilf.github.io/starlette-admin/user-guide/validations/
