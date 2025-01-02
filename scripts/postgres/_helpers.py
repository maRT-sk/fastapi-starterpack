import shutil
import subprocess

from loguru import logger

POSTGRES_CONTAINER_NAME = "my-postgres"


def check_docker() -> None:
    """Check if Docker CLI is installed and Docker Desktop is running."""
    if not shutil.which("docker"):
        logger.error("Preflight check: Docker CLI is not installed or not in PATH. Install Docker first.")
        raise SystemExit(1)

    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Preflight check: Docker CLI is installed, and Docker Desktop is running.")
    except subprocess.CalledProcessError as e:
        logger.error("Preflight check: Docker Desktop is not running. Please start it and try again.")
        raise SystemExit(1) from e


if __name__ == "__main__":
    check_docker()
