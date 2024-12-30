class SecretValidationError(Exception):
    """Custom exception for errors related to ProtectedSecret validation."""

    def __init__(self, message: str):
        super().__init__(message)


class ProtectedSecret:
    """Securely holds a string value with validation and obfuscation for safe handling."""

    def __init__(self, value: str):
        self._validate_complexity(value)
        self._value = value

    @staticmethod
    def _validate_complexity(value: str) -> None:
        """Validates the complexity of the secret. Raises an error if invalid."""

        if len(value) < 12:  # noqa: PLR2004
            raise SecretValidationError("Secret must be at least 12 characters long.")

        if not any(char.isupper() for char in value):
            raise SecretValidationError("Secret must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            raise SecretValidationError("Secret must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            raise SecretValidationError("Secret must contain at least one digit.")

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}('**********')"

    def __str__(self) -> str:
        return self._value

    def __bool__(self) -> bool:
        return bool(self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProtectedSecret):
            return NotImplemented
        return self._value == str(other)

    def __len__(self) -> int:
        return len(self._value)

    def masked(self, visible_chars: int = 4) -> str:
        """Returns a masked version of the secret, revealing only the last few characters."""
        masked_length = max(0, len(self._value) - visible_chars)
        return "*" * masked_length + self._value[-visible_chars:]
