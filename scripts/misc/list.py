# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# "toml~=0.10.0",
# ]
# ///


from pathlib import Path
from typing import Any

import toml
from loguru import logger


def list_scripts() -> None:
    """Reads and lists available task names from 'pyproject.toml' under the 'taskipy' section."""
    logger.info("Fetching available tasks from 'pyproject.toml'")

    try:
        data: dict[str, Any] = toml.load(Path("pyproject.toml"))
        tasks = data["tool"]["taskipy"]["tasks"]
        task_names = list(tasks.keys())
        print("Available tasks:\n" + "\n".join(task_names))
    except (FileNotFoundError, KeyError, toml.TomlDecodeError) as err:
        raise ValueError(f"Error reading tasks from 'pyproject.toml': {err}") from err


if __name__ == "__main__":
    list_scripts()
