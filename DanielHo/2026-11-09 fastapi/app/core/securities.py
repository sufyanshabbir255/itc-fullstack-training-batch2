# core\security.py

"""
app/core/security.py
--------------------

Security utilities:

    - Password hashing
    - Password verification
    - JWT creation
"""

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

def hash_password(
    password: str,
) -> str:
    """
    Convert a plain-text password into
    a secure bcrypt hash.
    """

    return pwd_context.hash(password)


# ---------------------------------------------------------------------------
# Password Verification
# ---------------------------------------------------------------------------

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Compare a plain password against
    a stored bcrypt hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ---------------------------------------------------------------------------
# Create JWT Access Token
# ---------------------------------------------------------------------------

def create_access_token(
    data: dict,
) -> str:
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    to_encode.update(
        {"exp": expire}
    )
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_refresh_token(
    data: dict,
) -> str:
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )
    to_encode.update(
        {"exp": expire}
    )
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )