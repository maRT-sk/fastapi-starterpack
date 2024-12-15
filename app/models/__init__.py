from importlib import import_module
from pathlib import Path


def import_models_modules() -> None:
    """
    Dynamically imports all Python files in the models directory as modules, excluding '__init__.py'.
    """
    models_path = Path(__file__).parent
    for model_file in models_path.glob("*.py"):
        if model_file.name != "__init__.py" and model_file.suffix == ".py":
            import_module(f"app.models.{model_file.stem}")
