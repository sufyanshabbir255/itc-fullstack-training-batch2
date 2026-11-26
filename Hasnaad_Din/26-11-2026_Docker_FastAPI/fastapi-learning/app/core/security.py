# added by Din: password hashing and (next step) JWT tokens
import bcrypt


def hash_password(password: str) -> str:
    """Turn a plain password into a bcrypt hash we can store."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """True if the typed password matches the stored hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

# added by Din: JWT access and refresh tokens
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import auth_settings


def create_access_token(username: str) -> str:
    """Short-lived pass (15 min) sent with every request."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "type": "access", "exp": expire}
    return jwt.encode(payload, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)


def create_refresh_token(username: str) -> str:
    """Long-lived pass (7 days) used ONLY to get a new pair."""
    expire = datetime.now(timezone.utc) + timedelta(days=auth_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": username, "type": "refresh", "jti": str(uuid.uuid4()), "exp": expire}
    return jwt.encode(payload, auth_settings.REFRESH_SECRET_KEY, algorithm=auth_settings.ALGORITHM)