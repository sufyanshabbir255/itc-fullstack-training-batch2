"""Password hashing (passlib/bcrypt) and JWT creation/decoding (python-jose)."""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from app.core.config import settings

TokenType = Literal["access", "refresh"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- passwords ----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------- JWT ----------
class TokenPayload(BaseModel):
    sub: str               # user id
    jti: str               # unique token id -> issued_tokens row
    type: TokenType
    role: str
    scopes: list[str] = []
    exp: int
    iat: int


class CreatedToken(BaseModel):
    token: str
    jti: str
    expires_at: datetime


def _secret_for(token_type: TokenType) -> str:
    return settings.SECRET_KEY if token_type == "access" else settings.REFRESH_SECRET_KEY


def create_token(
    *, subject: str | int, role: str, scopes: list[str], token_type: TokenType, expires_delta: timedelta
) -> CreatedToken:
    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta
    jti = uuid.uuid4().hex
    claims = {
        "sub": str(subject),
        "jti": jti,
        "type": token_type,
        "role": role,
        "scopes": scopes,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(claims, _secret_for(token_type), algorithm=settings.ALGORITHM)
    return CreatedToken(token=token, jti=jti, expires_at=expires_at)


def create_access_token(subject: str | int, role: str, scopes: list[str]) -> CreatedToken:
    return create_token(
        subject=subject, role=role, scopes=scopes, token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str | int, role: str, scopes: list[str]) -> CreatedToken:
    return create_token(
        subject=subject, role=role, scopes=scopes, token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str, expected_type: TokenType) -> TokenPayload:
    """Verify signature + expiry and return the payload. Raises JWTError on any problem."""
    raw = jwt.decode(token, _secret_for(expected_type), algorithms=[settings.ALGORITHM])
    try:
        payload = TokenPayload(**raw)
    except ValidationError as exc:
        raise JWTError("Malformed token payload") from exc
    if payload.type != expected_type:
        raise JWTError("Wrong token type")
    return payload
