from typing import Any, Dict, List, Tuple

from src.config import CONFIG
from src.persistence.jsonl_repository import read_jsonl, append_jsonl, update_one, delete_one
from src.persistence.audit_logger import log_event
from src.utils.validators import validate_airport, validate_date_yyyy_mm_dd, validate_time_hhmm

def list_all_flights() -> List[Dict[str, Any]]:
    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    return read_jsonl(flights_path)

def search_flights(origin: str, dest: str, date_str: str, airline: str = "", max_price: int = 999999) -> Tuple[bool, str, List[Dict[str, Any]]]:
    ok, msg = validate_airport(origin)
    if not ok:
        return False, msg, []
    ok, msg = validate_airport(dest)
    if not ok:
        return False, msg, []
    ok, msg = validate_date_yyyy_mm_dd(date_str)
    if not ok:
        return False, msg, []

    origin = origin.strip().upper()
    dest = dest.strip().upper()
    airline = (airline or "").strip().upper()

    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    rows = read_jsonl(flights_path)

    results: List[Dict[str, Any]] = []
    for f in rows:
        if f.get("from") != origin:
            continue
        if f.get("to") != dest:
            continue
        if f.get("date") != date_str:
            continue
        if airline and str(f.get("airline", "")).upper() != airline:
            continue

        seats_left = int(f.get("seats_left", 0))
        if seats_left <= 0:
            continue

        base_price = int(f.get("base_price", 0))
        if base_price <= 0:
            continue
        if base_price > max_price:
            continue

        results.append(f)

    if not results:
        return True, "No matching flights found.", []
    return True, f"Found {len(results)} flights.", results

def admin_add_flight(flight: Dict[str, Any]) -> Tuple[bool, str]:
    required = ["flight_id", "from", "to", "date", "airline", "depart", "arrive", "seats_total", "seats_left", "base_price"]
    for k in required:
        if k not in flight:
            return False, f"Missing field: {k}"

    ok, msg = validate_airport(str(flight["from"]))
    if not ok:
        return False, msg
    ok, msg = validate_airport(str(flight["to"]))
    if not ok:
        return False, msg
    ok, msg = validate_date_yyyy_mm_dd(str(flight["date"]))
    if not ok:
        return False, msg
    ok, msg = validate_time_hhmm(str(flight["depart"]))
    if not ok:
        return False, msg
    ok, msg = validate_time_hhmm(str(flight["arrive"]))
    if not ok:
        return False, msg

    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    for existing in read_jsonl(flights_path):
        if existing.get("flight_id") == flight["flight_id"]:
            return False, "Flight ID already exists."

    append_jsonl(flights_path, flight)
    log_event("ADMIN_ADD_FLIGHT", f"flight_id={flight['flight_id']}")
    return True, "Flight added."

def admin_update_flight(flight_id: str, patch: Dict[str, Any]) -> Tuple[bool, str]:
    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    if not flight_id:
        return False, "Flight ID required."
    ok = update_one(flights_path, "flight_id", flight_id, patch)
    if ok:
        log_event("ADMIN_UPDATE_FLIGHT", f"flight_id={flight_id} keys={list(patch.keys())}")
        return True, "Flight updated."
    return False, "Flight not found."

def admin_delete_flight(flight_id: str) -> Tuple[bool, str]:
    flights_path = f"{CONFIG.data_dir}/{CONFIG.flights_file}"
    if not flight_id:
        return False, "Flight ID required."
    ok = delete_one(flights_path, "flight_id", flight_id)
    if ok:
        log_event("ADMIN_DELETE_FLIGHT", f"flight_id={flight_id}")
        return True, "Flight deleted."
    return False, "Flight not found."
