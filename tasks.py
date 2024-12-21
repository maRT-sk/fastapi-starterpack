# TODO: Evaluate the possibility of using a different task runner

import logging
import os
import shutil
from pathlib import Path

from invoke import Context  # type: ignore[attr-defined]
from invoke import Result  # type: ignore[attr-defined]
from invoke import task  # type: ignore[attr-defined]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Determine whether to use a pseudo-terminal
is_pty = os.name != "nt"  # 'nt' indicates Windows


##### Temporary solution, these values will be retrieved from .env via UV: https://github.com/astral-sh/uv/issues/9994
postgres_container_name = "my-postgres"
postgres_user = "myuser"
postgres_password = "mypassword"
postgres_db = "mydatabase"
#####


@task
def alembic_up(c: Context) -> None:
    """Creates an Alembic migration with a user-specified message and optionally upgrades the database."""
    # Prompt for the migration message
    migration_message = input("Enter migration message: ").strip()
    if not migration_message:
        logging.error("Migration message cannot be empty. Aborting.")
        raise SystemExit(1)

    # Create Alembic migration revision
    logging.info(f'Creating migration with message: "{migration_message}"...')
    try:
        c.run(f'uv run alembic revision --autogenerate -m "{migration_message}"', pty=is_pty)
        logging.info("Migration created successfully.")
    except Exception as e:
        logging.error(f"Failed to create migration. Aborting. Error: {e}")
        return

    # Prompt to proceed with the upgrade
    proceed_with_upgrade = input("Proceed with upgrade? (y/n): ").strip().lower()
    if proceed_with_upgrade == "y":
        print("Upgrading database...")
        try:
            c.run("uv run alembic upgrade head", pty=is_pty)
            logging.info("Database upgraded successfully.")
        except Exception as e:
            logging.error(f"Database upgrade failed. Error: {e}")
    else:
        logging.info("Upgrade aborted.")


@task
def check_docker(c: Context) -> None:
    """Check if Docker CLI is installed and Docker Desktop is running."""
    if not shutil.which("docker"):
        logging.error("Docker CLI is not installed or not in PATH. Install Docker first.")
        raise SystemExit(1)

    result_is_docker_running: Result | None = c.run("docker info", warn=True, hide=True, pty=is_pty)
    if not result_is_docker_running or result_is_docker_running.failed:
        logging.error("Docker Desktop is not running. Please start it and try again.")
        raise SystemExit(1)

    logging.info("Docker CLI is installed, and Docker Desktop is running.")


@task(pre=[check_docker])
def db_create(
    c: Context,
    container_name: str = postgres_container_name,
    user: str = postgres_user,
    password: str = postgres_password,
    db: str = postgres_db,
) -> None:
    """Creates and starts a Docker container for PostgreSQL."""
    c.run(
        f"docker run --name {container_name} "
        f"-e POSTGRES_USER={user} "
        f"-e POSTGRES_PASSWORD={password} "
        f"-e POSTGRES_DB={db} "
        f"-p 5432:5432 -d postgres",
        pty=is_pty,
    )
    logging.info(f"PostgreSQL container '{container_name}' created and started successfully.")


@task(pre=[check_docker])
def db_start(c: Context, container_name: str = postgres_container_name) -> None:
    """Starts an existing PostgreSQL Docker container."""
    c.run(f"docker start {container_name}", pty=is_pty)
    logging.info(f"PostgreSQL container '{container_name}' started successfully.")


@task(pre=[check_docker])
def db_remove(c: Context, container_name: str = postgres_container_name) -> None:
    """Stops and removes the running PostgreSQL Docker container after confirmation."""
    confirmation = input(f"Do you want to stop and remove '{container_name}'? (y/n): ").strip().lower()
    if confirmation in ["y", "yes"]:
        c.run(f"docker stop {container_name}", pty=is_pty)
        c.run(f"docker rm {container_name}", pty=is_pty)
        logging.info(f"PostgreSQL container '{container_name}' removed successfully.")
    else:
        logging.info("Operation canceled.")


@task
def check_node_tools(c: Context) -> None:
    """Verifies the availability of Node.js tools (npm and npx)."""
    if not shutil.which("npm"):
        logging.error("npm is not installed or not in PATH. Install Node.js and npm first.")
        raise SystemExit(1)

    if not shutil.which("npx"):
        logging.error("npx is not installed or not in PATH. Install Node.js and npm first.")
        raise SystemExit(1)


@task(pre=[check_node_tools])
def tw_install(c: Context) -> None:
    """Installs Tailwind CSS as a dependency and initializes its configuration file."""
    # Proceed with Tailwind installation
    c.run("npm install -D tailwindcss", pty=is_pty)
    logging.info("Tailwind CSS installed successfully.")
    c.run("npx tailwindcss init", pty=is_pty)
    logging.info("Tailwind CSS configuration initialized successfully.")


@task(pre=[check_node_tools])
def tw_watch(
    c: Context, _input: str = "./app/static/css/input.css", _output: str = "./app/static/css/styles.css"
) -> None:
    """Watches the input CSS file and project files for changes and updates the output CSS file."""
    if not Path(_input).exists():
        logging.error(f"Input file '{_input}' does not exist. ")
        raise SystemExit(1)
    logging.info(f"Watching '{_input}' and project files for changes and writing output to '{_output}'.")
    c.run(f"npx tailwindcss -i {_input} -o {_output} --watch", pty=is_pty)


@task
def generate_req(c: Context) -> None:
    """Generates requirements.txt from pyproject.toml."""
    c.run("uv lock", pty=is_pty)
    c.run("uv pip compile pyproject.toml -o requirements.txt", pty=is_pty)
    logging.info("requirements.txt generated successfully.")
