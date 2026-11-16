import pytest
import time
from circuit_breaker import CircuitBreaker

# 1. Start Closed
def test_circuit_starts_closed():
    breaker = CircuitBreaker()
    assert breaker.state == "CLOSED"
    assert breaker.failure_count == 0

# 2. Opens After 3 Failures
def failing_service():
    raise Exception("Service Down")

# 3. Open Circuit Fails Fast
def test_circuit_opens_after_threshold():
    breaker = CircuitBreaker(
        failure_threshold=3
    )
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(failing_service)
    assert breaker.state == "OPEN"
    assert breaker.failure_count == 3

# 4. Successful Call Resets Failures
def success_service():
    return {"status": "ok"}

def test_success_resets_failure_count():
    breaker = CircuitBreaker()
    try:
        breaker.call(failing_service)
    except Exception:
        pass
    assert breaker.failure_count == 1
    breaker.call(success_service)
    assert breaker.failure_count == 0

# 5. Half-open returns to Closed
def test_half_open_to_closed():
    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout=1
    )
    with pytest.raises(Exception):
        breaker.call(failing_service)
    assert breaker.state == "OPEN"
    time.sleep(1.1)
    result = breaker.call(success_service)
    assert result == {"status": "ok"}
    assert breaker.state == "CLOSED"

# 6. Half-Open Reopens on Failure
def test_half_open_reopens_if_failure():

    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout=1
    )

    with pytest.raises(Exception):
        breaker.call(failing_service)

    assert breaker.state == "OPEN"

    time.sleep(1.1)

    with pytest.raises(Exception):
        breaker.call(failing_service)

    assert breaker.state == "OPEN"