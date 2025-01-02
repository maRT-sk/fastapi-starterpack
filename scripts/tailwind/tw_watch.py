# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# ]
# ///

import os
from pathlib import Path

from _helpers import check_node_tools
from loguru import logger


def tw_watch(_input: str = "./app/static/css/input.css", _output: str = "./app/static/css/styles.css") -> None:
    """Watches the input CSS file and project files for changes and updates the output CSS file."""
    check_node_tools()  # Ensure node tools are available

    if not Path(_input).exists():
        logger.error(f"Input file '{_input}' does not exist.")
        raise SystemExit(1)

    logger.info(f"Watching '{_input}' and project files for changes and writing output to '{_output}'.")
    os.system(f"npx tailwindcss -i {_input} -o {_output} --watch")


if __name__ == "__main__":
    tw_watch()
