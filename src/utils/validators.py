import re
from typing import Tuple

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
AIRPORT_RE = re.compile(r"^[A-Z]{3}$")

def validate_email(email: str) -> Tuple[bool, str]:
    email = (email or "").strip().lower()
    if not email:
        return False, "Email is required."
    if not EMAIL_RE.match(email):
        return False, "Invalid email format."
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    password = password or ""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    if not (has_upper and has_lower and has_digit):
        return False, "Password must include upper, lower, and digit."
    return True, ""

def validate_airport(code: str) -> Tuple[bool, str]:
    code = (code or "").strip().upper()
    if not code:
        return False, "Airport code is required."
    if not AIRPORT_RE.match(code):
        return False, "Airport code must be 3 uppercase letters."
    return True, ""

def validate_date_yyyy_mm_dd(date_str: str) -> Tuple[bool, str]:
    date_str = (date_str or "").strip()
    if not date_str:
        return False, "Date is required."
    parts = date_str.split("-")
    if len(parts) != 3:
        return False, "Date must be YYYY-MM-DD."
    y, m, d = parts
    if not (y.isdigit() and m.isdigit() and d.isdigit()):
        return False, "Date must be numeric."
    yi, mi, di = int(y), int(m), int(d)
    if yi < 2020 or yi > 2035:
        return False, "Year out of allowed range."
    if mi < 1 or mi > 12:
        return False, "Month out of range."
    if di < 1 or di > 31:
        return False, "Day out of range."
    return True, ""

def validate_seat(seat_no: str) -> Tuple[bool, str]:
    seat_no = (seat_no or "").strip().upper()
    if not seat_no:
        return False, "Seat number required."
    if len(seat_no) < 2 or len(seat_no) > 4:
        return False, "Seat format invalid."
    if not seat_no[:-1].isdigit():
        return False, "Seat row must be numeric."
    if not seat_no[-1].isalpha():
        return False, "Seat letter must be alphabetic."
    return True, ""
