from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class IssuedToken(Base):
    """Whitelist of issued tokens. A token is valid only while its row exists;
    revoking a token = deleting its row."""

    __tablename__ = "issued_tokens"

    jti: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_type: Mapped[str] = mapped_column(String(10))           # "access" | "refresh"
    paired_jti: Mapped[str] = mapped_column(String(64), index=True)  # the other token of the pair
    scopes: Mapped[str] = mapped_column(String(500), default="")     # space-separated
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
