from fastapi import FastAPI
from circuit_breaker import CircuitBreaker
import payment_service


app = FastAPI(title="Circuit Breaker Demo")


# Create one Circuit Breaker instance
breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=10
)


# API 1: Make Payment
@app.get("/pay")
def pay():

    result = breaker.call(payment_service.make_payment)

    return result


# API 2: Stop Payment Service
@app.post("/service/down")
def service_down():

    message = payment_service.stop_service()

    return {"message": message}


# API 3: Start Payment Service
@app.post("/service/up")
def service_up():

    message = payment_service.start_service()

    return {"message": message}


# API 4: Check Circuit Breaker Status
@app.get("/breaker/status")
def breaker_status():

    return breaker.get_status()


@app.get("/")
def home():

    return {
        "message": "Circuit Breaker Application is running"
    }
