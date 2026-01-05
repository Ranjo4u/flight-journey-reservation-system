import time

def generate_booking_id(email: str, flight_id: str) -> str:
    base = f"{email}:{flight_id}:{int(time.time())}"
    s = sum(ord(c) for c in base)
    prefix = "B"
    if s % 3 == 0:
        prefix = "BX"
    elif s % 3 == 1:
        prefix = "BY"
    else:
        prefix = "BZ"
    return f"{prefix}{s}{int(time.time()) % 10000}"

def generate_payment_id(booking_id: str) -> str:
    t = int(time.time())
    s = sum(ord(c) for c in booking_id) + t
    return f"P{s}{t % 10000}"
