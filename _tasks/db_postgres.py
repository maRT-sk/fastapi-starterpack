import os
import shutil

from invoke import Context  # type: ignore[attr-defined]
from invoke import Result  # type: ignore[attr-defined]
from invoke import task  # type: ignore[attr-defined]

from _tasks import is_pty
from _tasks import task_logger

POSTGRES_CONTAINER_NAME = "my-postgres"


@task
def check_docker(c: Context) -> None:
    """Check if Docker CLI is installed and Docker Desktop is running."""
    if not shutil.which("docker"):
        task_logger.error("Preflight check: Docker CLI is not installed or not in PATH. Install Docker first.")
        raise SystemExit(1)

    result_is_docker_running: Result | None = c.run("docker info", warn=True, hide=True, pty=is_pty)
    if not result_is_docker_running or result_is_docker_running.failed:
        task_logger.error("Preflight check: Docker Desktop is not running. Please start it and try again.")
        raise SystemExit(1)

    task_logger.info("Preflight check:: Docker CLI is installed, and Docker Desktop is running.")


# @task()
# def check_db_running(c: Context, container_name: str = POSTGRES_CONTAINER_NAME) -> None:
#     """Checks if the PostgreSQL Docker container is running locally."""
#     result = c.run(
#         f"docker ps --filter name={container_name} --format '{{{{.Names}}}}'", hide=True, warn=True, pty=is_pty
#     )
#
#     if container_name in result.stdout.strip():
#         task_logger.info(f"Preflight check: PostgreSQL container '{container_name}' is running.")
#         return
#     else:
#         task_logger.error(f"Preflight check: PostgreSQL container '{container_name}' is not running.")
#         task_logger.error("Preflight check: Ensure the container is started with the 'db_start' task.")
#         raise SystemExit(1)


@task(pre=[check_docker])
def db_create(
    c: Context,
    container_name: str = POSTGRES_CONTAINER_NAME,
) -> None:
    """Creates and starts a Docker container for PostgreSQL."""

    user: str | None = os.getenv("POSTGRES_USER", None)
    password: str | None = os.getenv("POSTGRES_PASSWORD", None)
    db: str | None = os.getenv("POSTGRES_DB", None)

    if not user or not password or not db:
        raise ValueError(
            "Missing one or more required environment variables: " "POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB"
        )

    c.run(
        f"docker run --name {container_name} "
        f"-e POSTGRES_USER={user} "
        f"-e POSTGRES_PASSWORD={password} "
        f"-e POSTGRES_DB={db} "
        f"-p 5432:5432 -d postgres",
        pty=is_pty,
    )
    task_logger.info(f"PostgreSQL container '{container_name}' created and started successfully.")


@task(pre=[check_docker])
def db_start(c: Context, container_name: str = POSTGRES_CONTAINER_NAME) -> None:
    """Starts an existing PostgreSQL Docker container."""
    c.run(f"docker start {container_name}", pty=is_pty)
    task_logger.info(f"PostgreSQL container '{container_name}' started successfully.")


@task(pre=[check_docker])
def db_remove(c: Context, container_name: str = POSTGRES_CONTAINER_NAME) -> None:
    """Stops and removes the running PostgreSQL Docker container after confirmation."""
    confirmation = input(f"Do you want to stop and remove '{container_name}'? (y/n): ").strip().lower()
    if confirmation in ["y", "yes"]:
        c.run(f"docker stop {container_name}", pty=is_pty)
        c.run(f"docker rm {container_name}", pty=is_pty)
        task_logger.info(f"PostgreSQL container '{container_name}' removed successfully.")
    else:
        task_logger.info("Operation canceled.")
