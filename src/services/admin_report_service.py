from typing import Any, Dict, List
import os

from src.config import CONFIG
from src.persistence.jsonl_repository import read_jsonl

def _bookings_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.bookings_file}"

def _flights_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.flights_file}"

def _audit_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.audit_file}"

def report_all_bookings() -> List[Dict[str, Any]]:
    return read_jsonl(_bookings_path())

def report_revenue_summary() -> str:
    bookings = read_jsonl(_bookings_path())
    total_paid = 0
    paid_count = 0
    cancelled = 0
    pending = 0

    for b in bookings:
        status = b.get("status")
        amt = int(b.get("amount", 0))
        if status == "PAID":
            total_paid += amt
            paid_count += 1
        elif status == "CANCELLED":
            cancelled += 1
        else:
            pending += 1

    return (
        "=== Revenue Summary ===\n"
        f"Total PAID bookings: {paid_count}\n"
        f"Total revenue (PAID): {total_paid}\n"
        f"Pending bookings: {pending}\n"
        f"Cancelled bookings: {cancelled}"
    )

def report_seat_utilisation() -> str:
    flights = read_jsonl(_flights_path())
    if not flights:
        return "No flights available."

    lines = ["=== Seat Utilisation ==="]
    for f in flights:
        total = int(f.get("seats_total", 0))
        left = int(f.get("seats_left", 0))
        used = max(total - left, 0)
        util = (used / total * 100.0) if total > 0 else 0.0
        lines.append(f"{f.get('flight_id')} | {f.get('from')}->{f.get('to')} | {f.get('date')} | used={used}/{total} ({util:.1f}%)")
    return "\n".join(lines)

def report_audit_summary() -> str:
    path = _audit_path()
    if not os.path.exists(path):
        return "No audit log available."

    counts: Dict[str, int] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue
            event = parts[1]
            counts[event] = counts.get(event, 0) + 1

    lines = ["=== Audit Log Summary ==="]
    for k in sorted(counts.keys()):
        lines.append(f"{k}: {counts[k]}")
    return "\n".join(lines)
