import time


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None

    def allow_request(self):
        if self.state == "OPEN":
            seconds_open = time.time() - self.opened_at
            if seconds_open >= self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        return True

    def record_success(self):
        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None

    def record_failure(self):
        if self.state == "HALF_OPEN":
            self.open_circuit()
            return
        self.failure_count = self.failure_count + 1
        if self.failure_count >= self.failure_threshold:
            self.open_circuit()

    def open_circuit(self):
        self.state = "OPEN"
        self.opened_at = time.time()