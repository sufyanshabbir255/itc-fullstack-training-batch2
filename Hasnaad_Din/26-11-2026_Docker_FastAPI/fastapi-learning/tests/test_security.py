# added by Din: tests for CSRF double-submit
from fastapi.testclient import TestClient
from app.main import app


def test_transfer_without_token_is_refused():
    client = TestClient(app)
    response = client.post("/transfer")
    assert response.status_code == 403


def test_transfer_with_matching_token_works():
    client = TestClient(app)
    token = client.get("/csrf-token").json()["csrf_token"]
    response = client.post("/transfer", headers={"X-CSRF-Token": token})
    assert response.status_code == 200


def test_transfer_with_wrong_token_is_refused():
    client = TestClient(app)
    client.get("/csrf-token")
    response = client.post("/transfer", headers={"X-CSRF-Token": "wrong-token"})
    assert response.status_code == 403
    