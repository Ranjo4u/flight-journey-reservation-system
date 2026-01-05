from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: str
    email: str
    flight_id: str
    passenger_name: str
    passengers: int
    seat_no: str
    amount: int
    status: str
