# Steps to run
**1. Prerequisite:** Python 3.10 or newer (`python3 --version`).

**2. Go into the project folder**
```bash
cd '.\2026-11-18 rate limiter\'
```

**3. Create and activate a virtual environment**
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate    

# Windows
python3 -m venv venv
venv\Scripts\activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Start the server** (either command works)
```bash
fastapi dev app/main.py
# or
uvicorn app.main:app --reload
```

**6. Make requests**
```bash
GET /
GET /
GET /
```

Will get the reply:
```json
{
    "message"   : "Hello FastAPI"
}
```

On the 4th attempt:
```json
{
  "error": "Rate limit exceeded"
}
```