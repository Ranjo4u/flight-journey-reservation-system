from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    data_dir: str = "data"
    users_file: str = "users.jsonl"
    flights_file: str = "flights.jsonl"
    bookings_file: str = "bookings.jsonl"
    payments_file: str = "payments.jsonl"
    audit_file: str = "audit.log"

CONFIG = AppConfig()
