# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# "python-dotenv~=1.0.0"
# ]
# ///

import os

from _helpers import POSTGRES_CONTAINER_NAME
from _helpers import check_docker
from dotenv import load_dotenv
from loguru import logger


def db_create(container_name: str = POSTGRES_CONTAINER_NAME) -> None:
    """Creates and starts a Docker container for PostgreSQL."""
    check_docker()
    load_dotenv()
    user: str | None = os.getenv("POSTGRES_USER")
    password: str | None = os.getenv("POSTGRES_PASSWORD")
    db: str | None = os.getenv("POSTGRES_DB")

    if not user or not password or not db:
        raise ValueError(
            "Missing one or more required environment variables: " "POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB"
        )

    os.system(
        f"docker run --name {container_name} "
        f"-e POSTGRES_USER={user} "
        f"-e POSTGRES_PASSWORD={password} "
        f"-e POSTGRES_DB={db} "
        f"-p 5432:5432 -d postgres"
    )
    logger.info(f"PostgreSQL container '{container_name}' created and started successfully.")


if __name__ == "__main__":
    db_create()
