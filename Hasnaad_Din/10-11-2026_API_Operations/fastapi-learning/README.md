# FastAPI Learning Project

Covers: **APIRouter**, **path operations (GET/POST/PUT/PATCH/DELETE)**, **response_model**, **status codes**, and **OpenAPI docs**. Every file has comments explaining what it does and why.

## Folder structure

```
fastapi-learning/
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── app/
│   ├── __init__.py
│   ├── main.py               # Creates FastAPI app, OpenAPI config, mounts routers
│   ├── core/
│   │   └── config.py         # App settings (title, version, API prefix)
│   ├── schemas/              # Pydantic models (request bodies + response_model)
│   │   ├── item.py           # ItemCreate / ItemUpdate / ItemPatch / ItemOut
│   │   └── user.py           # UserCreate / UserOut (password hidden)
│   ├── db/
│   │   └── fake_db.py        # In-memory "database" + sample data
│   └── routers/              # APIRouter modules
│       ├── __init__.py       # Combines routers into api_router
│       ├── items.py          # Full CRUD, all HTTP methods & status codes
│       └── users.py          # response_model filtering demo
└── tests/
    └── test_api.py           # Automated tests with TestClient
```

## Request flow

```
Client → main.py (app) → /api/v1 prefix → api_router → items.router (/items)
       → path operation function → validates body/params with schemas
       → returns dict → response_model filters/validates → JSON + status code
```

## Steps to run

**1. Prerequisite:** Python 3.10 or newer (`python3 --version`).

**2. Go into the project folder**
```bash
cd fastapi-learning
```

**3. Create and activate a virtual environment**
```bash
python3 -m venv venv
#source venv/bin/activate          # macOS / Linux
venv\Scripts\activate           # Windows
```

**4. Install dependencies**
```bash
#pip install -r requirements.txt
python -m pip install --upgrade pip
pip install fastapi uvicorn email-validator httpx pytest
```

**5. Start the server** (either command works)
```bash
#fastapi dev app/main.py
# or
uvicorn app.main:app --reload
```
`--reload` / `dev` restarts the server automatically when you save a file.

**6. Open in your browser**

| URL | What it is |
|---|---|
| http://127.0.0.1:8000/docs | Swagger UI – try every endpoint |
| http://127.0.0.1:8000/redoc | ReDoc documentation |
| http://127.0.0.1:8000/openapi.json | Raw OpenAPI spec |

**7. Run the tests**
```bash
pytest -v
```

**8. Stop the server:** `Ctrl + C`. Deactivate the venv with `deactivate`.

## Endpoints

| Method | Path | Status | Concept |
|---|---|---|---|
| GET | `/api/v1/items/` | 200 | Query params `skip`, `limit`, `in_stock` |
| GET | `/api/v1/items/{item_id}` | 200 / 404 | Path param + HTTPException |
| POST | `/api/v1/items/` | 201 / 409 / 422 | Request body, validation |
| PUT | `/api/v1/items/{item_id}` | 200 / 404 | Full replace |
| PATCH | `/api/v1/items/{item_id}` | 200 / 404 | Partial update (`exclude_unset`) |
| DELETE | `/api/v1/items/{item_id}` | 204 / 404 | Empty response |
| GET | `/api/v1/items/search/by-name?q=` | 200 | `deprecated=True` in docs |
| POST | `/api/v1/users/` | 201 / 409 | `response_model` hides password |
| GET | `/api/v1/users/` | 200 | List with `response_model=list[UserOut]` |
| GET | `/health` | 200 | Route defined directly on `app` |

## Try it with curl

```bash
# List items
curl http://127.0.0.1:8000/api/v1/items/

# Create (201)
curl -X POST http://127.0.0.1:8000/api/v1/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyboard", "price": 49.99}'

# Partial update (200)
curl -X PATCH http://127.0.0.1:8000/api/v1/items/1 \
  -H "Content-Type: application/json" -d '{"price": 899}'

# Delete (204)
curl -i -X DELETE http://127.0.0.1:8000/api/v1/items/2

# Validation error (422) – price must be > 0
curl -X POST http://127.0.0.1:8000/api/v1/items/ \
  -H "Content-Type: application/json" -d '{"name": "Bad", "price": -5}'

# Create user – note: no password in the response
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "romesh", "email": "romesh@example.com", "password": "supersecret123"}'
```

## Key concepts summary

- **APIRouter** – a mini-app for one feature. Has its own `prefix` and `tags`; plugged in with `include_router()`. Prefixes stack (`/api/v1` + `/items`).
- **Path operation** – decorator (`@router.get`, `.post`, `.put`, `.patch`, `.delete`) + function.
- **Parameters** – in the URL path → path param; a Pydantic model → JSON body; anything else → query param.
- **response_model** – validates the output, removes undeclared fields (security), and documents the response.
- **status_code** – sets the success code (201 for create, 204 for delete). Errors use `HTTPException`. Invalid input gives 422 automatically.
- **OpenAPI docs** – generated from your code: `summary`, `description`, `tags`, `responses`, `deprecated`, `openapi_tags`, and the Pydantic models.

> Data is stored in memory, so it resets each time the server restarts.
