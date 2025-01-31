from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

import bcrypt


# Workaround for issue: https://github.com/pyca/bcrypt/issues/684
@dataclass
class BcryptVersion:
    __version__: str

    def __init__(self) -> None:
        try:
            self.__version__ = version("bcrypt")
        except PackageNotFoundError:
            self.__version__ = "unknown"


bcrypt.__about__ = BcryptVersion()  # type: ignore[attr-defined]
