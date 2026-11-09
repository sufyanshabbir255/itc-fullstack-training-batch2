"""
tests/test_api.py
-----------------
Automated tests using FastAPI's TestClient (built on httpx).

TestClient calls the app directly in-process – no server needs to be running.
Each test checks BOTH the status code and the response body, which is exactly
what response_model and status_code control.

Run with:   pytest -v
"""

from fastapi.testclient import TestClient

from app.main import app

BASE = "/api/v1"


def test_health():
    with TestClient(app) as client:  # `with` triggers the lifespan (seed data)
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


def test_item_crud_flow():
    with TestClient(app) as client:
        # CREATE -> 201
        r = client.post(f"{BASE}/items/", json={"name": "Test Pen", "price": 2.5})
        assert r.status_code == 201
        item = r.json()
        assert item["name"] == "Test Pen"
        assert "id" in item and "created_at" in item
        item_id = item["id"]

        # DUPLICATE -> 409
        r = client.post(f"{BASE}/items/", json={"name": "Test Pen", "price": 2.5})
        assert r.status_code == 409

        # READ -> 200
        r = client.get(f"{BASE}/items/{item_id}")
        assert r.status_code == 200

        # PATCH (only price) -> 200, name unchanged
        r = client.patch(f"{BASE}/items/{item_id}", json={"price": 3.0})
        assert r.status_code == 200
        assert r.json()["price"] == 3.0
        assert r.json()["name"] == "Test Pen"

        # PUT (full replace) -> 200
        r = client.put(
            f"{BASE}/items/{item_id}",
            json={"name": "Blue Pen", "price": 4.0, "in_stock": False},
        )
        assert r.status_code == 200
        assert r.json()["name"] == "Blue Pen"

        # DELETE -> 204, empty body
        r = client.delete(f"{BASE}/items/{item_id}")
        assert r.status_code == 204
        assert r.content == b""

        # READ AGAIN -> 404
        r = client.get(f"{BASE}/items/{item_id}")
        assert r.status_code == 404


def test_validation_error_returns_422():
    with TestClient(app) as client:
        # price must be > 0
        r = client.post(f"{BASE}/items/", json={"name": "Bad", "price": -1})
        assert r.status_code == 422


def test_query_params():
    with TestClient(app) as client:
        r = client.get(f"{BASE}/items/?limit=2")
        assert r.status_code == 200
        assert len(r.json()) <= 2


def test_response_model_hides_password():
    with TestClient(app) as client:
        r = client.post(
            f"{BASE}/users/",
            json={"username": "romesh", "email": "romesh@example.com", "password": "supersecret123"},
        )
        assert r.status_code == 201
        body = r.json()
        assert "password" not in body
        assert "hashed_password" not in body


def test_openapi_schema_available():
    with TestClient(app) as client:
        r = client.get("/openapi.json")
        assert r.status_code == 200
        assert f"{BASE}/items/" in r.json()["paths"]
