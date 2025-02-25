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
