"""Token storage in the database.

Every issued token is whitelisted in the `issued_tokens` table by its `jti`.
A token is accepted only while its row exists, so revocation = DELETE the row.
Access and refresh tokens are issued in pairs and point to each other via
`paired_jti`, so logging out removes both. Expired rows are purged on each login.
"""
from datetime import datetime, timezone

from jose import JWTError
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    TokenPayload,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.token import IssuedToken
from app.schemas.token import TokenPair


class InvalidRefreshToken(Exception):
    pass


class TokenService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- issue ----------
    def issue_pair(self, user_id: int, role: str, scopes: list[str]) -> TokenPair:
        self.purge_expired()
        access = create_access_token(user_id, role, scopes)
        refresh = create_refresh_token(user_id, role, scopes)
        scope_str = " ".join(scopes)

        self.db.add_all([
            IssuedToken(jti=access.jti, user_id=user_id, token_type="access",
                        paired_jti=refresh.jti, scopes=scope_str, expires_at=access.expires_at),
            IssuedToken(jti=refresh.jti, user_id=user_id, token_type="refresh",
                        paired_jti=access.jti, scopes=scope_str, expires_at=refresh.expires_at),
        ])
        self.db.commit()

        return TokenPair(
            access_token=access.token,
            refresh_token=refresh.token,
            expires_in=settings.access_token_ttl_seconds,
            scope=scope_str,
        )

    # ---------- validate ----------
    def is_access_token_active(self, jti: str) -> bool:
        row = self.db.get(IssuedToken, jti)
        return row is not None and row.token_type == "access"

    # ---------- refresh (rotation) ----------
    def consume_refresh_token(self, refresh_token: str) -> tuple[TokenPayload, list[str]]:
        """Validate a refresh token and revoke it together with its access token (single use).

        If a correctly signed refresh token is no longer stored, it was already used or
        revoked — treated as possible theft, so every session of that user is revoked.
        """
        try:
            payload = decode_token(refresh_token, expected_type="refresh")
        except JWTError as exc:
            raise InvalidRefreshToken("Invalid refresh token") from exc

        row = self.db.get(IssuedToken, payload.jti)
        if row is None or row.token_type != "refresh":
            self.revoke_all_for_user(int(payload.sub))
            raise InvalidRefreshToken("Refresh token revoked or already used")

        scopes = row.scopes.split() if row.scopes else []
        # rowcount check: only one concurrent request can consume the token
        deleted = self.db.execute(delete(IssuedToken).where(IssuedToken.jti == row.jti)).rowcount
        if deleted == 0:
            self.db.rollback()
            raise InvalidRefreshToken("Refresh token revoked or already used")
        self.db.execute(delete(IssuedToken).where(IssuedToken.jti == row.paired_jti))
        self.db.commit()
        return payload, scopes

    # ---------- revoke ----------
    def revoke_session(self, access_payload: TokenPayload) -> None:
        """Logout: delete the access token and the refresh token issued with it."""
        row = self.db.get(IssuedToken, access_payload.jti)
        jtis = [access_payload.jti] + ([row.paired_jti] if row else [])
        self.db.execute(delete(IssuedToken).where(IssuedToken.jti.in_(jtis)))
        self.db.commit()

    def revoke_all_for_user(self, user_id: int) -> int:
        """Logout everywhere: delete every token the user owns."""
        count = self.db.execute(delete(IssuedToken).where(IssuedToken.user_id == user_id)).rowcount
        self.db.commit()
        return count

    def purge_expired(self) -> None:
        now = datetime.now(timezone.utc)
        self.db.execute(delete(IssuedToken).where(IssuedToken.expires_at < now))

