from dataclasses import dataclass

@dataclass
class Payment:
    payment_id: str
    booking_id: str
    email: str
    amount: int
    status: str
    reason: str = ""
