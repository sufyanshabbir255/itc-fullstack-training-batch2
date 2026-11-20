service_available = True
def make_payment():
    global service_available
    if not service_available:
        raise Exception("Payment service is DOWN")

    return "Payment successful!"


def stop_service():

    global service_available
    service_available = False

    return "Payment service is now DOWN"


def start_service():

    global service_available
    service_available = True

    return "Payment service is now UP"
