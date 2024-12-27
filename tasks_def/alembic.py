from invoke import Context  # type: ignore[attr-defined]
from invoke import task  # type: ignore[attr-defined]

from tasks_def import is_pty
from tasks_def import task_logger

POSTGRES_CONTAINER_NAME = "my-postgres"


@task
def alembic_up(c: Context) -> None:
    """Creates an Alembic migration with a user-specified message and optionally upgrades the database."""
    # Prompt for the migration message
    migration_message = input("Enter migration message: ").strip()
    if not migration_message:
        task_logger.error("Migration message cannot be empty. Aborting.")
        raise SystemExit(1)

    # Create Alembic migration revision
    task_logger.info(f'Creating migration with message: "{migration_message}"...')
    try:
        c.run(f'uv run alembic revision --autogenerate -m "{migration_message}"', pty=is_pty)
        task_logger.info("Migration created successfully.")
    except Exception as e:
        task_logger.error(f"Failed to create migration. Aborting. Error: {e}")
        return

    # Prompt to proceed with the upgrade
    proceed_with_upgrade = input("Proceed with upgrade? (y/n): ").strip().lower()
    if proceed_with_upgrade == "y":
        print("Upgrading database...")
        try:
            c.run("uv run alembic upgrade head", pty=is_pty)
            task_logger.info("Database upgraded successfully.")
        except Exception as e:
            task_logger.error(f"Database upgrade failed. Error: {e}")
    else:
        task_logger.info("Upgrade aborted.")
