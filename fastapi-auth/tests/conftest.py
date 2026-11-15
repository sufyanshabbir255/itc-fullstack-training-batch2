import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.permissions import Role
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import User

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(engine)
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db):
    def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    # No context manager -> lifespan (real DB init) is not run.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(db):
    def _make(email: str, password: str = "password123", role: Role = Role.USER) -> User:
        user = User(email=email, hashed_password=hash_password(password), role=role.value)
        db.add(user)
        db.commit()
        return user
    return _make


def login(client, email, password="password123", scope: str | None = None):
    data = {"username": email, "password": password}
    if scope is not None:
        data["scope"] = scope
    return client.post("/api/v1/auth/token", data=data)


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
