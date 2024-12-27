from pathlib import Path

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret


class AppConfig:
    """
    A configuration class that centralizes app settings and provides a unified way to manage environment variables
    for both local development and production.

    The class detects and uses a `.env` file for local development,
    while falling back to environment variables when deployed on a server.
    This ensures flexibility and security by separating configuration from code.
    """

    def __init__(self) -> None:
        # Check if a `.env` file exists in the project directory.
        # If it exists, its path is assigned, otherwise `None` is used (environment variables will be loaded).
        config_path: str | None = ".env" if Path(".env").exists() else None
        config = Config(config_path)

        self.SECRET_KEY = config("SECRET_KEY", cast=Secret)
        self.ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
        self.DEBUG = config("DEBUG", cast=bool, default=False)
        self.DB_ECHO = config("DB_ECHO", cast=bool, default=False)
        self.LOG_FILE = config("LOG_FILE", default="logs/app_{time}.log")
        self.LOG_LEVEL = config("LOG_LEVEL", default="INFO")
        self.DATABASE_URL = config("DATABASE_URL")


# Create a global instance of the configuration class that can be imported into other modules.
app_config = AppConfig()
