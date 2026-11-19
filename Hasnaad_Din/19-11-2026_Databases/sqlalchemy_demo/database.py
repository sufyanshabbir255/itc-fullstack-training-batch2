# database.py - the connection to PostgreSQL (one place, used by everything else)
import getpass

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

password = getpass.getpass("postgres password: ")

# [CONNECTION] "postgresql+psycopg" = PostgreSQL through the psycopg driver you used on 12-11
DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="itc_practice",
)

engine = create_engine(DATABASE_URL, echo=False)      # echo=True prints every SQL statement it runs
SessionLocal = sessionmaker(bind=engine)               # a session = one conversation with the database


class Base(DeclarativeBase):                           # every table class inherits from this
    pass