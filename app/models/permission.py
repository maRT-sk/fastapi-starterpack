from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.models import Base
from app.models._links import user_permission_table


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    # Relationships
    users = relationship("User", secondary=user_permission_table, back_populates="user_permissions", lazy="select")
