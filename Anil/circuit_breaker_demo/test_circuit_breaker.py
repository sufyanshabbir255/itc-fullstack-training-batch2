
import time
import pytest

from circuit_breaker import CircuitBreaker, CircuitState


@pytest.fixture
def breaker():
    return CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=0.1
    )


# Test 1: Successful service call
def test_success(breaker):

    def payment():
        return "Payment successful"

    result = breaker.call(payment)

    assert result["source"] == "service"
    assert breaker.state == CircuitState.CLOSED


# Test 2: Three failures should OPEN the circuit
def test_three_failures_open_circuit(breaker):

    def failed_payment():
        raise Exception("Service unavailable")

    for _ in range(3):
        breaker.call(failed_payment)

    assert breaker.state == CircuitState.OPEN
    assert breaker.failure_count == 3


# Test 3: OPEN circuit should block service calls
def test_open_circuit_blocks_calls(breaker):

    call_count = 0

    def failed_payment():
        nonlocal call_count
        call_count += 1
        raise Exception("Service unavailable")

    for _ in range(3):
        breaker.call(failed_payment)

    result = breaker.call(failed_payment)

    assert result["source"] == "fallback"
    assert call_count == 3
    assert breaker.state == CircuitState.OPEN


# Test 4: HALF_OPEN should close after successful call
def test_half_open_success(breaker):

    def failed_payment():
        raise Exception("Service unavailable")

    for _ in range(3):
        breaker.call(failed_payment)

    time.sleep(0.15)

    def successful_payment():
        return "Payment successful"

    result = breaker.call(successful_payment)

    assert result["source"] == "service"
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0


# Test 5: HALF_OPEN should OPEN again after failure
def test_half_open_failure(breaker):

    def failed_payment():
        raise Exception("Service unavailable")

    for _ in range(3):
        breaker.call(failed_payment)

    time.sleep(0.15)

    result = breaker.call(failed_payment)

    assert result["source"] == "fallback"
    assert breaker.state == CircuitState.OPEN
