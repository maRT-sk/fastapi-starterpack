# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# ]
# ///

import os

from _helpers import check_node_tools
from loguru import logger


def tw_install() -> None:
    """Installs Tailwind CSS as a dependency and initializes its configuration file."""
    check_node_tools()  # Ensure node tools are available
    os.system("npm install -D tailwindcss")
    logger.info("Tailwind CSS installed successfully.")
    os.system("npx tailwindcss init")
    logger.info("Tailwind CSS configuration initialized successfully.")


if __name__ == "__main__":
    tw_install()
