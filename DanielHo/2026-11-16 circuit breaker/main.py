from fastapi import FastAPI, HTTPException
import requests
from circuit_breaker import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=10
)

app = FastAPI()

# @app.get("/order")
# def create_order():
#     response = requests.get(
#         "http://localhost:8001/pay",
#     timeout=2
#     )
#     return response.json()

def call_payment():
    response = requests.get(
        "http://localhost:8001/pay",
        timeout=2
    )
    response.raise_for_status()
    return response.json()

@app.get("/order")
def create_order():
    try:
        return breaker.call(call_payment)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

@app.get("/breaker")
def breaker_state():
    return {
        "state": breaker.state,
        "failures": breaker.failure_count,
    }
