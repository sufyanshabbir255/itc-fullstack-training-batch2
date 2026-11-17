import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):

        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    def call(self, service_function):

        # 1. Check if circuit is OPEN
        if self.state == CircuitState.OPEN:

            elapsed_time = time.time() - self.last_failure_time

            if elapsed_time < self.recovery_timeout:
                return {
                    "message": "Payments are paused. Please try later.",
                    "source": "fallback"
                }

            # Recovery timeout completed
            self.state = CircuitState.HALF_OPEN
            print("Circuit changed to HALF_OPEN")

        # 2. Try calling the actual service
        try:

            result = service_function()

            # 3. If successful, close the circuit
            self.failure_count = 0
            self.state = CircuitState.CLOSED
            self.last_failure_time = None

            return {
                "message": result,
                "source": "service"
            }

        except Exception as error:

            self.failure_count += 1
            self.last_failure_time = time.time()

            print("Service failure:", error)

            # 4. Open circuit after threshold failures
            if self.failure_count >= self.failure_threshold:

                self.state = CircuitState.OPEN
                print("Circuit changed to OPEN")

            return {
                "message": "Payment service unavailable",
                "source": "fallback"
            }
    def get_status(self):

        return {
            "state": self.state.value,
            "failure_count": self.failure_count
        }
