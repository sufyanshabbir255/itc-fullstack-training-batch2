from fastapi import FastAPI

from circuit_breaker import CircuitBreaker

app = FastAPI(title="Circuit Breaker Demo")

breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

service_is_down = False


def payment_service():
    if service_is_down:
        raise Exception("Payment service is not responding")
    return {"payment": "accepted"}

@app.post("/service/down")
def break_service():
    global service_is_down
    service_is_down = True
    return {"service_is_down": service_is_down}


@app.post("/service/up")
def fix_service():
    global service_is_down
    service_is_down = False
    return {"service_is_down": service_is_down}


@app.get("/breaker/status")
def breaker_status():
    return {
        "state": breaker.state,
        "failure_count": breaker.failure_count,
        "failure_threshold": breaker.failure_threshold,
        "recovery_timeout": breaker.recovery_timeout,
    }

@app.get("/pay")
def pay():
    if not breaker.allow_request():
        return {
            "source": "fallback",
            "message": "Payments are paused. Please try again later.",
            "state": breaker.state,
        }

    try:
        result = payment_service()
        breaker.record_success()
        return {"source": "service", "result": result, "state": breaker.state}
    except Exception:
        breaker.record_failure()
        return {
            "source": "fallback",
            "message": "Payment service failed. Please try again later.",
            "state": breaker.state,
        }