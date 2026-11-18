## Steps to run
**1. Prerequisite:** Python 3.10 or newer (`python3 --version`).

**2. Go into the project folder**
```bash
cd .\DanielHo\2026-11-16 circuit breaker
```

**3. Create and activate a virtual environment**
```bash
# macOS / Linux
python3 -m venv .venv
source venv/bin/activate

# Windows
python3 -m venv .venv
venv\Scripts\activate           
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Start the server** (either command works)**
```bash
fastapi dev app/main.py
# or
uvicorn app.main:app --reload
```
> `--reload` / `dev` restarts the server automatically when you save a file

**6a. Make 'payment'**
```bash
http://localhost:8001/pay
```

```json
{
  "message": "Payment successful"
}
```

**6b. Make 'order'**
```bash
http://localhost:8000/order
```

```bash
{
  "message": "Payment successful"
}
```

**6c. check 'breaker'**
```bash
http://localhost:8000/breaker
```

```bash
{
  "state": "CLOSED",
  "failures": 0
}
```

**7. Kill 'payment' service**<br>
In terrminal running
> http://localhost:8001

```bash
CTRL+C
```

**8a. Call 'order' service **
```bash
http://localhost:8000/order
```

**8b. check 'breaker'**
```bash
http://localhost:8000/breaker
```

```bash
{
  "state": "CLOSED",
  "failures": 1
}
```

Retry steps 8a and 8b **two** additional times

**9. Check 'breaker'**
```bash
{
  "state":"OPEN"
  ,"failures":3
}
```