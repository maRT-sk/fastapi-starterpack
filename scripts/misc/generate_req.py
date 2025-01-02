# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# ]
# ///

import os

from loguru import logger


def generate_req() -> None:
    """Generates requirements.txt from pyproject.toml."""
    os.system("uv lock")
    os.system("uv pip compile pyproject.toml -o requirements.txt")
    logger.info("requirements.txt generated successfully.")


if __name__ == "__main__":
    generate_req()
