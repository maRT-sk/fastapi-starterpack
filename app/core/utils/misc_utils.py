from importlib import import_module
from pathlib import Path
from typing import Any

import toml


def get_version_from_pyproject() -> str:
    """Retrieve the version value from the 'pyproject.toml' file."""
    try:
        data: dict[str, Any] = toml.load(Path("pyproject.toml"))
        version = data["project"]["version"]
        if not isinstance(version, str):
            raise ValueError("Invalid version format in 'pyproject.toml'.")
        return version
    except (FileNotFoundError, KeyError, toml.TomlDecodeError) as err:
        raise ValueError(f"Error reading version from 'pyproject.toml': {err}") from err


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
