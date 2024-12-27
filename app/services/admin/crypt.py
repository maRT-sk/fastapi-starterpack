import secrets

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain-text password matches the hashed password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_random_hashed_password() -> str:
    """Generate a random bcrypt-hashed password."""
    random_password = secrets.token_urlsafe(16)
    hashed_password = bcrypt.hashpw(random_password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")
