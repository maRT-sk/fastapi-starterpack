from datetime import UTC
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import HTTPException
from fastapi import status
from passlib.context import CryptContext

from app.core.config import app_config

# Constants
SECRET_KEY = str(app_config.SECRET_KEY)
ALGORITHM = "HS256"


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


# TODO: needs to be integrated
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token with optional expiration."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# TODO: needs to be integrated
def verify_jwt(token: str) -> dict:
    """Verify the validity of a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, UTC) < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
