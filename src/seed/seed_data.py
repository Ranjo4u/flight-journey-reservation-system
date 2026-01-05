from src.config import CONFIG
from src.persistence.jsonl_repository import read_jsonl, append_jsonl
from src.persistence.audit_logger import log_event

def seed_if_empty() -> None:
    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    rows = read_jsonl(flights_path)
    if rows:
        return

    sample = [
        {
            "flight_id": "F1001", "from": "LHR", "to": "JFK", "date": "2026-02-14",
            "airline": "BRITJET", "depart": "10:30", "arrive": "13:10",
            "seats_total": 10, "seats_left": 10, "base_price": 420
        },
        {
            "flight_id": "F1002", "from": "LGW", "to": "CDG", "date": "2026-02-14",
            "airline": "EUROAIR", "depart": "08:00", "arrive": "10:20",
            "seats_total": 12, "seats_left": 12, "base_price": 90
        },
        {
            "flight_id": "F1003", "from": "MAN", "to": "DXB", "date": "2026-03-01",
            "airline": "SKYWAYS", "depart": "21:00", "arrive": "07:40",
            "seats_total": 8, "seats_left": 8, "base_price": 310
        }
    ]
    for f in sample:
        append_jsonl(flights_path, f)

    # Optional: seed one admin user (comment out if you don't want it)
    # You can register admin via CLI too.
    log_event("SEED_FLIGHTS", "inserted=3")
