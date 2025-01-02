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


def db_start(container_name: str = POSTGRES_CONTAINER_NAME) -> None:
    """Starts an existing PostgreSQL Docker container."""
    check_docker()
    os.system(f"docker start {container_name}")
    logger.info(f"PostgreSQL container '{container_name}' started successfully.")


if __name__ == "__main__":
    db_start()
