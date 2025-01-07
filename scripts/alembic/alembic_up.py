# /// script
# requires-python = ">=3.12"
# dependencies = [
# "loguru~=0.7.0",
# ]
# ///

import os
import subprocess
import sys

from loguru import logger

os.environ["VIRTUAL_ENV"] = ""  # Clearing VIRTUAL_ENV, required for consistent behavior with Alembic and UV


def alembic_up() -> None:
    """Creates an Alembic migration with a user-specified message and optionally upgrades the database."""
    # Prompt for the migration message
    migration_message = input("Enter migration message: ").strip()
    if not migration_message:
        logger.error("Migration message cannot be empty. Aborting.")
        sys.exit(1)

    # Create Alembic migration revision
    logger.info(f'Creating migration with message: "{migration_message}"...')
    try:
        result = subprocess.run(
            ["uv", "run", "alembic", "revision", "--autogenerate", "-m", migration_message],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("Migration created successfully.")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create migration. Error: {e.stderr.strip()}")
        sys.exit(1)

    # Prompt to proceed with the upgrade
    proceed_with_upgrade = input("Proceed with upgrade? (y/n): ").strip().lower()
    if proceed_with_upgrade in ["y", "yes"]:
        logger.info("Upgrading database...")
        try:
            result = subprocess.run(
                ["uv", "run", "alembic", "upgrade", "head"],
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info("Database upgraded successfully.")
            logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Database upgrade failed. Error: {e.stderr.strip()}")
            logger.warning("Remember to check and delete the generated migration file.")
            sys.exit(1)
    else:
        logger.info("Upgrade aborted!")
        logger.warning("Remember to run 'alembic upgrade head' or manage/delete the generated migration file.")


if __name__ == "__main__":
    alembic_up()
