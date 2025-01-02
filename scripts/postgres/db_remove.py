# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0"
# ]
# ///


import os

from _helpers import POSTGRES_CONTAINER_NAME
from _helpers import check_docker
from loguru import logger


def db_remove(container_name: str = POSTGRES_CONTAINER_NAME) -> None:
    """Stops and removes the running PostgreSQL Docker container after confirmation."""
    check_docker()

    confirmation = input(f"Do you want to stop and remove '{container_name}'? (y/n): ").strip().lower()
    if confirmation in ["y", "yes"]:
        os.system(f"docker stop {container_name}")
        os.system(f"docker rm {container_name}")
        logger.info(f"PostgreSQL container '{container_name}' removed successfully.")
    else:
        logger.info("Operation canceled.")


if __name__ == "__main__":
    db_remove()
