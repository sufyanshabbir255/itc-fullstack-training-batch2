import time

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=3,
        recovery_timeout=10
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.last_failure_time = None

        self.state = "CLOSED"
    def call(self, func):
        if self.state == "OPEN":
            elapsed = (
                time.time()
                - self.last_failure_time
            )
            if elapsed > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception(
                    "Circuit is OPEN"
                )
        try:
            result = func()
            self.failure_count = 0
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
            return result
        except Exception:
            self.failure_count += 1
            print(
                f"State={self.state}", 
                f"Failures={self.failure_count}"
            )
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("Circuit OPENED")
            raise