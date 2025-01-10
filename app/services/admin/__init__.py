from dataclasses import dataclass

import bcrypt


# Workaround for issue: https://github.com/pyca/bcrypt/issues/684
@dataclass
class BcryptVersion:
    __version__: str = bcrypt.__version__


bcrypt.__about__ = BcryptVersion()
