from sqlalchemy import select

from app.core.config import settings
from app.core.permissions import Role
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import User  # noqa: F401  (registers models on Base.metadata)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    if not (settings.FIRST_ADMIN_EMAIL and settings.FIRST_ADMIN_PASSWORD):
        return
    with SessionLocal() as db:
        exists = db.scalar(select(User).where(User.email == settings.FIRST_ADMIN_EMAIL))
        if not exists:
            db.add(User(
                email=settings.FIRST_ADMIN_EMAIL,
                full_name="Administrator",
                hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
                role=Role.ADMIN.value,
            ))
            db.commit()
