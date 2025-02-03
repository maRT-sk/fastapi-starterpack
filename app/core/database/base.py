from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

# Define ORM Base
Base = declarative_base(cls=AsyncAttrs)
