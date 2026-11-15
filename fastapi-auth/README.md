# FastAPI JWT Auth — access/refresh tokens, revocation, scopes & roles

Production-style auth starter built with **FastAPI**, **python-jose**, **passlib (bcrypt)**
and **SQLAlchemy 2.0**.

## Features

| Concern | Implementation |
|---|---|
| Password hashing | `passlib` `CryptContext(schemes=["bcrypt"])` — `app/core/security.py` |
| JWT | `python-jose`, separate secrets for access & refresh tokens, `jti`, `type`, `role`, `scopes` claims |
| Login | `OAuth2PasswordRequestForm` at `POST /api/v1/auth/token` (works with Swagger "Authorize") |
| Bearer auth | `OAuth2PasswordBearer(tokenUrl=..., scopes=SCOPES)` — `app/api/deps.py` |
| Token storage | Every token whitelisted in the `issued_tokens` DB table by `jti` |
| Revocation | Delete the token rows — logout, logout-all, role change, deactivation, password change |
| Refresh | Rotation (single use) + **reuse detection** (replayed refresh token revokes all user sessions) |
| `current_user` | `get_current_user` / `get_current_active_user` dependencies |
| Scopes | `Security(dep, scopes=[...])` + `SecurityScopes` check against token claims |
| Roles | `user`, `moderator`, `admin`; `require_roles(...)` dependency; role → max-scopes map |

## Project structure

```
fastapi-auth/
├── app/
│   ├── main.py                    # FastAPI app + lifespan (DB init)
│   ├── core/
│   │   ├── config.py              # pydantic-settings (.env)
│   │   ├── security.py            # bcrypt hashing, JWT create/decode
│   │   └── permissions.py         # Role enum, SCOPES, ROLE_SCOPES, resolve_scopes()
│   ├── db/
│   │   ├── base.py                # DeclarativeBase
│   │   ├── session.py             # engine, SessionLocal, get_db
│   │   └── init_db.py             # create tables, bootstrap admin
│   ├── models/                    # SQLAlchemy models (User, Item, IssuedToken)
│   ├── schemas/                   # Pydantic models (user, token, item)
│   ├── services/
│   │   └── token_service.py       # issue / validate / rotate / revoke tokens
│   └── api/
│       ├── deps.py                # oauth2_scheme, get_current_user, require_roles
│       └── v1/
│           ├── router.py
│           └── endpoints/
│               ├── auth.py        # register, token, refresh, logout, logout-all
│               ├── users.py       # /me, admin user management
│               └── items.py       # scope-protected example resource
├── tests/                         # pytest (in-memory SQLite)
├── .env.example
└── requirements.txt
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # set real secrets
uvicorn app.main:app --reload
```

No external services needed — users, items and tokens are stored in SQLite (`app.db`).

Open http://localhost:8000/docs → **Authorize** → log in with email/password and tick the scopes you want.

**Tests:** `pytest` (uses in-memory SQLite).

## Endpoints

| Method | Path | Protection |
|---|---|---|
| POST | `/api/v1/auth/register` | public |
| POST | `/api/v1/auth/token` | public (form: `username`, `password`, optional `scope`) |
| POST | `/api/v1/auth/refresh` | refresh token in JSON body |
| POST | `/api/v1/auth/logout` | any valid access token |
| POST | `/api/v1/auth/logout-all` | any valid access token |
| GET / PATCH | `/api/v1/users/me` | scope `me` |
| GET | `/api/v1/users/` | role admin/moderator + scope `users:read` |
| PATCH | `/api/v1/users/{id}/role` | role admin + scope `users:write` |
| PATCH | `/api/v1/users/{id}/deactivate` · `/activate` | role admin + scope `users:write` |
| GET | `/api/v1/items/` | scope `items:read` (own items; mod/admin see all) |
| POST / DELETE | `/api/v1/items/` · `/{id}` | scope `items:write` (owner or mod/admin) |

## Roles → scopes

| Role | Max scopes |
|---|---|
| user | `me`, `items:read`, `items:write` |
| moderator | user scopes + `users:read` |
| admin | all, incl. `users:write` |

If no `scope` is sent at login the token gets every scope the role allows. Requesting a scope the
role doesn't have returns `400`. Role checks read the role from the DB, so a role change applies
immediately, and changing a role also revokes the user's existing tokens.

## Token storage

Issued tokens are whitelisted in the `issued_tokens` table (`app/models/token.py`):

| Column | Meaning |
|---|---|
| `jti` | token ID (primary key) |
| `user_id` | owner (for logout-all) |
| `token_type` | `access` / `refresh` |
| `paired_jti` | the other token of the pair (logout removes both) |
| `scopes` | granted scopes (reused on refresh) |
| `expires_at` | expired rows are purged on each login |

A token is accepted only if its signature/expiry are valid **and** its row exists. Revoking = deleting the row.

## Example with curl

```bash
# register
curl -X POST localhost:8000/api/v1/auth/register -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","password":"password123"}'

# login (optionally restrict scopes)
curl -X POST localhost:8000/api/v1/auth/token \
  -d 'username=me@example.com&password=password123&scope=me items:read'

# call API
curl localhost:8000/api/v1/users/me -H "Authorization: Bearer <access_token>"

# refresh (rotates both tokens)
curl -X POST localhost:8000/api/v1/auth/refresh -H 'Content-Type: application/json' \
  -d '{"refresh_token":"<refresh_token>"}'

# logout (deletes access + paired refresh token)
curl -X POST localhost:8000/api/v1/auth/logout -H "Authorization: Bearer <access_token>"
```

## Production notes

- Use long random secrets; consider RS256 with key rotation for multi-service setups.
- Swap SQLite for PostgreSQL by changing `DATABASE_URL` (add Alembic for migrations).
- At high traffic, token lookups can move to Redis later — only `token_service.py` needs to change.
- Add rate limiting on `/auth/token` and `/auth/refresh`.
- Serve over HTTPS only.
