import shutil
import sys

from loguru import logger


def check_node_tools() -> None:
    """Verifies the availability of Node.js tools (npm and npx)."""
    if not shutil.which("npm"):
        logger.error("Preflight check: npm is not installed or not in PATH. Install Node.js and npm first.")
        sys.exit(1)

    if not shutil.which("npx"):
        logger.error("Preflight check: npx is not installed or not in PATH. Install Node.js and npm first.")
        sys.exit(1)
