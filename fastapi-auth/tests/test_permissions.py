from app.core.permissions import Role
from tests.conftest import auth, login


def test_scope_restricted_token(client, make_user):
    make_user("a@x.com")
    token = login(client, "a@x.com", scope="items:read").json()["access_token"]
    assert client.get("/api/v1/items/", headers=auth(token)).status_code == 200
    r = client.post("/api/v1/items/", json={"title": "x"}, headers=auth(token))
    assert r.status_code == 403 and "items:write" in r.json()["detail"]
    assert client.get("/api/v1/users/me", headers=auth(token)).status_code == 403


def test_user_cannot_request_admin_scope(client, make_user):
    make_user("a@x.com")
    assert login(client, "a@x.com", scope="users:write").status_code == 400


def test_role_based_user_listing(client, make_user):
    make_user("user@x.com")
    make_user("mod@x.com", role=Role.MODERATOR)
    user_t = login(client, "user@x.com").json()["access_token"]
    mod_t = login(client, "mod@x.com").json()["access_token"]

    assert client.get("/api/v1/users/", headers=auth(user_t)).status_code == 403
    r = client.get("/api/v1/users/", headers=auth(mod_t))
    assert r.status_code == 200 and len(r.json()) == 2


def test_admin_changes_role_and_old_tokens_revoked(client, make_user):
    target = make_user("user@x.com")
    make_user("admin@x.com", role=Role.ADMIN)
    old_t = login(client, "user@x.com").json()["access_token"]
    admin_t = login(client, "admin@x.com").json()["access_token"]

    r = client.patch(f"/api/v1/users/{target.id}/role", json={"role": "moderator"}, headers=auth(admin_t))
    assert r.status_code == 200 and r.json()["role"] == "moderator"
    assert client.get("/api/v1/users/me", headers=auth(old_t)).status_code == 401

    new_t = login(client, "user@x.com").json()
    assert "users:read" in new_t["scope"].split()


def test_admin_without_scope_is_denied(client, make_user):
    target = make_user("user@x.com")
    make_user("admin@x.com", role=Role.ADMIN)
    admin_t = login(client, "admin@x.com", scope="me users:read").json()["access_token"]
    r = client.patch(f"/api/v1/users/{target.id}/role", json={"role": "admin"}, headers=auth(admin_t))
    assert r.status_code == 403


def test_deactivated_user_locked_out(client, make_user):
    target = make_user("user@x.com")
    make_user("admin@x.com", role=Role.ADMIN)
    user_t = login(client, "user@x.com").json()["access_token"]
    admin_t = login(client, "admin@x.com").json()["access_token"]
    assert client.patch(f"/api/v1/users/{target.id}/deactivate", headers=auth(admin_t)).status_code == 200
    assert client.get("/api/v1/users/me", headers=auth(user_t)).status_code == 401
    assert login(client, "user@x.com").status_code == 403


def test_item_ownership(client, make_user):
    make_user("a@x.com")
    make_user("b@x.com")
    make_user("mod@x.com", role=Role.MODERATOR)
    a = login(client, "a@x.com").json()["access_token"]
    b = login(client, "b@x.com").json()["access_token"]
    mod = login(client, "mod@x.com").json()["access_token"]

    item_id = client.post("/api/v1/items/", json={"title": "A's"}, headers=auth(a)).json()["id"]
    assert client.get("/api/v1/items/", headers=auth(b)).json() == []
    assert len(client.get("/api/v1/items/", headers=auth(mod)).json()) == 1
    assert client.delete(f"/api/v1/items/{item_id}", headers=auth(b)).status_code == 403
    assert client.delete(f"/api/v1/items/{item_id}", headers=auth(mod)).status_code == 204
