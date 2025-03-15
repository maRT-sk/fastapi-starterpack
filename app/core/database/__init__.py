from importlib import import_module
from pathlib import Path

from app.core.database import base
from app.core.database import health
from app.core.database import repository
from app.core.database import session

Base = base.Base
Repository = repository.Repository
get_session = session.get_session
check_db_ready = health.check_db_ready


# Automatically imports all model files to ensure Alembic can detect ORM models for migrations.
def import_models_modules() -> None:
    """Imports all Python modules with 'model' in their filename."""
    # TODO: Improve the base path calculation. Using parent.parent.parent is not ideal.
    for file in Path(__file__).parent.parent.parent.rglob("*model*.py"):
        try:
            import_module(
                f"app.{'.'.join(file.relative_to(Path(__file__).parent.parent.parent).with_suffix('').parts)}"
            )
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(f"Failed to import {file}. Error: {e}") from e


__all__ = ["Base", "Repository", "get_session", "import_models_modules", "check_db_ready"]
