from tests.conftest import auth, login


def test_register_and_login(client):
    r = client.post("/api/v1/auth/register", json={"email": "a@x.com", "password": "password123"})
    assert r.status_code == 201
    assert r.json()["role"] == "user"

    r = login(client, "a@x.com")
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert set(body["scope"].split()) == {"me", "items:read", "items:write"}

    me = client.get("/api/v1/users/me", headers=auth(body["access_token"]))
    assert me.status_code == 200 and me.json()["email"] == "a@x.com"


def test_wrong_password(client, make_user):
    make_user("a@x.com")
    assert login(client, "a@x.com", "nope-nope").status_code == 401


def test_duplicate_register(client, make_user):
    make_user("a@x.com")
    r = client.post("/api/v1/auth/register", json={"email": "a@x.com", "password": "password123"})
    assert r.status_code == 409


def test_refresh_rotation_and_reuse_detection(client, make_user):
    make_user("a@x.com")
    first = login(client, "a@x.com").json()

    r = client.post("/api/v1/auth/refresh", json={"refresh_token": first["refresh_token"]})
    assert r.status_code == 200
    second = r.json()

    # old access token was revoked with the old refresh token
    assert client.get("/api/v1/users/me", headers=auth(first["access_token"])).status_code == 401
    assert client.get("/api/v1/users/me", headers=auth(second["access_token"])).status_code == 200

    # reusing the old refresh token -> rejected AND all sessions revoked
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": first["refresh_token"]})
    assert r.status_code == 401
    assert client.get("/api/v1/users/me", headers=auth(second["access_token"])).status_code == 401


def test_access_token_cannot_be_used_as_refresh(client, make_user):
    make_user("a@x.com")
    tokens = login(client, "a@x.com").json()
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["access_token"]})
    assert r.status_code == 401


def test_logout_revokes_access_and_refresh(client, make_user):
    make_user("a@x.com")
    tokens = login(client, "a@x.com").json()
    assert client.post("/api/v1/auth/logout", headers=auth(tokens["access_token"])).status_code == 204
    assert client.get("/api/v1/users/me", headers=auth(tokens["access_token"])).status_code == 401
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r.status_code == 401


def test_logout_all(client, make_user):
    make_user("a@x.com")
    t1 = login(client, "a@x.com").json()
    t2 = login(client, "a@x.com").json()
    assert client.post("/api/v1/auth/logout-all", headers=auth(t1["access_token"])).status_code == 204
    for t in (t1, t2):
        assert client.get("/api/v1/users/me", headers=auth(t["access_token"])).status_code == 401


def test_invalid_token(client):
    assert client.get("/api/v1/users/me", headers=auth("garbage")).status_code == 401
    assert client.get("/api/v1/users/me").status_code == 401
