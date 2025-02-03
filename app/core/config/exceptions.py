class AppError:
    class MissingConfigurationError(Exception):
        """Raised when a required configuration key is missing."""

        pass

    class SecretValidationError(Exception):
        """Custom exception for errors related to ProtectedSecret validation."""

        def __init__(self, message: str):
            super().__init__(message)
