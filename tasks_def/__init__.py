import logging
import os
from pathlib import Path

# Determine whether to use a pseudo-terminal
is_pty = os.name != "nt"  # 'nt' indicates Windows


def load_env_file(env_file: str = ".env") -> None:
    """Manually load environment variables from a .env file."""
    env_path = Path(env_file)

    if not env_path.exists():
        raise FileNotFoundError(f"{env_file} file not found.")

    with env_path.open("r") as file:
        for line in file:
            stripped_line = line.strip()  # Use a new variable for the stripped line
            if not stripped_line or stripped_line.startswith("#"):
                continue
            key, value = stripped_line.split("=", 1)
            os.environ[key] = value


def configure_logger(name: str = "task_logger", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a logger that outputs to the console."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        formatter = logging.Formatter(fmt="%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


load_env_file()
task_logger = configure_logger()
