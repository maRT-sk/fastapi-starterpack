from importlib import import_module
from pathlib import Path


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
