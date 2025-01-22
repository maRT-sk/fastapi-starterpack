from importlib import import_module
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    """Base class for all the ORM models."""

    pass


def import_models_modules() -> None:
    """
    Dynamically imports all Python files in the models directory as modules, excluding '__init__.py'.
    """
    models_path = Path(__file__).parent
    for model_file in models_path.rglob("*.py"):
        if model_file.name != "__init__.py" and model_file.suffix == ".py":
            relative_path = model_file.relative_to(models_path.parent)
            module_path = f"app.{'.'.join(relative_path.with_suffix('').parts)}"
            try:
                import_module(module_path)
            except ModuleNotFoundError as e:
                raise ModuleNotFoundError(f"Failed to import module: {module_path}. Error: {e}") from e
