from dataclasses import dataclass

@dataclass
class Flight:
    flight_id: str
    origin: str
    destination: str
    date: str
    airline: str
    depart: str
    arrive: str
    seats_total: int
    seats_left: int
    base_price: int
