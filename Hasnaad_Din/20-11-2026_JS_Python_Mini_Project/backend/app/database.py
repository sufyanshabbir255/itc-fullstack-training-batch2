# database.py - the connection to PostgreSQL (same idea as the 19-11 ticket)
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DB_PASSWORD

DATABASE_URL = URL.create(
    "postgresql+pg8000",
    username="postgres",
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    database="mini_project_db",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# [DEPENDENCY] gives each request its own session, and always closes it afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()