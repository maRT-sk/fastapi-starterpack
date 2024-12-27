from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from app.models.demo.product import Product
from app.models.demo.product import ProductCreate
from app.models.permission import Permission
from app.models.user import User
from app.models.user import UserCreate

# from starlette_admin.contrib.sqlmodel import ModelView


class UserView(ModelView):
    fields = [
        User.username,
        User.full_name,
        User.email,
        User.password,
        User.is_active,
        User.is_superuser,
        User.user_permissions,
    ]
    exclude_fields_from_list = [User.password]


def attach_admin_views(admin_interface):
    admin_interface.add_view(UserView(User, pydantic_model=UserCreate))
    admin_interface.add_view(ModelView(Permission, pydantic_model=Permission))
    admin_interface.add_view(ModelView(Product, pydantic_model=ProductCreate))

    # TODO
    # Validation via pydantic_model does not work; it might be a Starlette Admin bug.
    # Documentation: https://jowilf.github.io/starlette-admin/user-guide/validations/
