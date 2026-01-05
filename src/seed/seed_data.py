import random
import hashlib
from datetime import date, timedelta

from src.config import CONFIG
from src.persistence.jsonl_repository import read_jsonl, append_jsonl, find_one
from src.persistence.audit_logger import log_event

def _hash_password(password: str, salt: str) -> str:
    raw = (salt + password).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def seed_if_empty() -> None:
    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    users_path = f"{CONFIG.data_dir}/{CONFIG.users_file}"

    # 1) Seed Admin (only once)
    admin_email = "admin@group7.com"
    if not find_one(users_path, "email", admin_email):
        salt = hashlib.md5(admin_email.encode("utf-8")).hexdigest()[:8]
        pw_hash = _hash_password("Admin1234", salt)
        append_jsonl(users_path, {
            "email": admin_email,
            "role": "admin",
            "salt": salt,
            "pw_hash": pw_hash,
            "failed_attempts": 0,
            "locked": False
        })
        log_event("SEED_ADMIN", f"email={admin_email}")

    # 2) Seed 10 traveller users (only if few users exist)
    if len(read_jsonl(users_path)) < 5:
        for i in range(1, 11):
            email = f"user{i}@demo.com"
            if find_one(users_path, "email", email):
                continue
            salt = hashlib.md5(email.encode("utf-8")).hexdigest()[:8]
            pw_hash = _hash_password("User1234", salt)
            append_jsonl(users_path, {
                "email": email,
                "role": "traveller",
                "salt": salt,
                "pw_hash": pw_hash,
                "failed_attempts": 0,
                "locked": False
            })
        log_event("SEED_USERS", "count=10")

    # 3) Seed flights (only if empty)
    if read_jsonl(flights_path):
        return

    airports = ["LHR", "LGW", "MAN", "BHX", "EDI", "GLA"]
    destinations = ["JFK", "DXB", "CDG", "AMS", "DEL", "SIN"]
    airlines = ["BRITJET", "EUROAIR", "SKYWAYS", "GLOBALFLY", "AEROX"]

    base_prices = {
        "JFK": (350, 650),
        "DXB": (300, 600),
        "DEL": (280, 550),
        "SIN": (400, 700),
        "CDG": (80, 180),
        "AMS": (90, 200)
    }

    today = date.today()
    flight_count = 0

    for i in range(1, 71):  # 70 flights
        origin = random.choice(airports)
        dest = random.choice(destinations)
        if origin == dest:
            continue

        days_ahead = random.randint(1, 120)
        flight_date = today + timedelta(days=days_ahead)

        airline = random.choice(airlines)
        seats_total = random.choice([120, 150, 180, 200])
        seats_left = random.randint(40, seats_total)

        price_min, price_max = base_prices[dest]
        base_price = random.randint(price_min, price_max)

        depart_hour = random.choice(["06", "09", "12", "15", "18", "21"])
        arrive_hour = str((int(depart_hour) + random.randint(2, 8)) % 24).zfill(2)

        flight = {
            "flight_id": f"F{1000 + i}",
            "from": origin,
            "to": dest,
            "date": flight_date.isoformat(),
            "airline": airline,
            "depart": f"{depart_hour}:00",
            "arrive": f"{arrive_hour}:30",
            "seats_total": seats_total,
            "seats_left": seats_left,
            "base_price": base_price
        }
        append_jsonl(flights_path, flight)
        flight_count += 1

    log_event("SEED_FLIGHTS", f"count={flight_count}")
