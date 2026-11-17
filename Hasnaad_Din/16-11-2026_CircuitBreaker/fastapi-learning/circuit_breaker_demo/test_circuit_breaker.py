import time

import pytest
from fastapi.testclient import TestClient

import breaker_app
from circuit_breaker import CircuitBreaker

client = TestClient(breaker_app.app)


@pytest.fixture(autouse=True)
def fresh_breaker():
    breaker_app.breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
    breaker_app.service_is_down = False


def test_closed_calls_pass_through():
    response = client.get("/pay")
    assert response.json()["source"] == "service"
    assert response.json()["state"] == "CLOSED"

def test_opens_after_threshold_failures():
    client.post("/service/down")
    client.get("/pay")
    client.get("/pay")
    assert breaker_app.breaker.state == "CLOSED"
    client.get("/pay")
    assert breaker_app.breaker.state == "OPEN"


def test_open_returns_fallback_without_calling_service():
    client.post("/service/down")
    for i in range(3):
        client.get("/pay")
    client.post("/service/up")
    response = client.get("/pay")
    assert response.json()["source"] == "fallback"
    assert response.json()["state"] == "OPEN"

def test_half_open_success_closes_circuit():
    client.post("/service/down")
    for i in range(3):
        client.get("/pay")
    client.post("/service/up")
    time.sleep(1.1)
    response = client.get("/pay")
    assert response.json()["source"] == "service"
    assert response.json()["state"] == "CLOSED"


def test_half_open_failure_reopens_circuit():
    client.post("/service/down")
    for i in range(3):
        client.get("/pay")
    time.sleep(1.1)
    response = client.get("/pay")
    assert response.json()["source"] == "fallback"
    assert response.json()["state"] == "OPEN"

def test_half_open_allows_only_one_trial_request():  # added by Din
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=1)
    breaker.record_failure()
    time.sleep(1.1)
    assert breaker.allow_request() is True
    assert breaker.allow_request() is False
    assert breaker.allow_request() is False