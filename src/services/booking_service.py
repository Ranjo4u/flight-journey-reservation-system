from typing import Any, Dict, List, Optional, Tuple

from src.config import CONFIG
from src.constants import BOOKING_STATUS_PENDING, BOOKING_STATUS_PAID, BOOKING_STATUS_CANCELLED
from src.persistence.jsonl_repository import read_jsonl, append_jsonl, update_one
from src.persistence.audit_logger import log_event
from src.utils.validators import validate_seat
from src.utils.id_generator import generate_booking_id
from src.utils.pricing_engine import dynamic_price

def _flights_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.flights_file}"

def _bookings_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.bookings_file}"

def _get_flight(flight_id: str) -> Optional[Dict[str, Any]]:
    for f in read_jsonl(_flights_path()):
        if f.get("flight_id") == flight_id:
            return f
    return None

def _seat_taken(flight_id: str, seat_no: str) -> bool:
    for b in read_jsonl(_bookings_path()):
        if b.get("flight_id") == flight_id and b.get("status") in (BOOKING_STATUS_PAID,):
            if b.get("seat_no") == seat_no:
                return True
    return False

def create_booking(email: str, flight_id: str, passenger_name: str, passengers: int, seat_no: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    email = (email or "").strip().lower()
    flight_id = (flight_id or "").strip().upper()
    passenger_name = (passenger_name or "").strip()
    seat_no = (seat_no or "").strip().upper()

    if not email or "@" not in email:
        return False, "Invalid email.", None
    if not flight_id:
        return False, "Flight ID required.", None
    if not passenger_name:
        return False, "Passenger name required.", None
    if passengers <= 0:
        return False, "Passengers must be at least 1.", None

    ok, msg = validate_seat(seat_no)
    if not ok:
        return False, msg, None

    flight = _get_flight(flight_id)
    if not flight:
        return False, "Flight not found.", None

    seats_left = int(flight.get("seats_left", 0))
    if seats_left <= 0:
        return False, "No seats left on this flight.", None

    if _seat_taken(flight_id, seat_no):
        return False, "Seat already booked (paid booking).", None

    base_price = int(flight.get("base_price", 0))
    final_unit = dynamic_price(base_price, str(flight.get("date", "")), str(flight.get("depart", "")), passengers)
    amount = final_unit * passengers

    booking_id = generate_booking_id(email, flight_id)
    booking = {
        "booking_id": booking_id,
        "email": email,
        "flight_id": flight_id,
        "passenger_name": passenger_name,
        "passengers": passengers,
        "seat_no": seat_no,
        "amount": amount,
        "status": BOOKING_STATUS_PENDING
    }
    append_jsonl(_bookings_path(), booking)

    # update seats_left: subtract passengers (branch-friendly)
    subtract = passengers if passengers > 1 else 1
    new_left = max(seats_left - subtract, 0)
    update_one(_flights_path(), "flight_id", flight_id, {"seats_left": new_left})

    log_event("BOOKING_CREATED", f"booking_id={booking_id} flight_id={flight_id} email={email} amount={amount}")
    return True, "Booking created (PENDING). Proceed to payment.", booking

def list_bookings_for_user(email: str) -> List[Dict[str, Any]]:
    email = (email or "").strip().lower()
    return [b for b in read_jsonl(_bookings_path()) if b.get("email") == email]

def get_booking(booking_id: str) -> Optional[Dict[str, Any]]:
    for b in read_jsonl(_bookings_path()):
        if b.get("booking_id") == booking_id:
            return b
    return None

def mark_paid(booking_id: str) -> bool:
    ok = update_one(_bookings_path(), "booking_id", booking_id, {"status": BOOKING_STATUS_PAID})
    if ok:
        log_event("BOOKING_PAID", f"booking_id={booking_id}")
    return ok

def cancel_booking(email: str, booking_id: str) -> Tuple[bool, str]:
    email = (email or "").strip().lower()
    booking = get_booking(booking_id)
    if not booking:
        return False, "Booking not found."
    if booking.get("email") != email:
        return False, "You can only cancel your own booking."

    status = booking.get("status")
    if status == BOOKING_STATUS_CANCELLED:
        return False, "Booking is already cancelled."
    if status == BOOKING_STATUS_PAID:
        # allow cancellation but mark cancelled; seat refunds not implemented to keep logic clear
        pass

    ok = update_one(_bookings_path(), "booking_id", booking_id, {"status": BOOKING_STATUS_CANCELLED})
    if ok:
        log_event("BOOKING_CANCELLED", f"booking_id={booking_id} email={email}")
        return True, "Booking cancelled."
    return False, "Failed to cancel booking."

def modify_booking_seat(email: str, booking_id: str, new_seat_no: str) -> Tuple[bool, str]:
    email = (email or "").strip().lower()
    new_seat_no = (new_seat_no or "").strip().upper()
    ok, msg = validate_seat(new_seat_no)
    if not ok:
        return False, msg

    booking = get_booking(booking_id)
    if not booking:
        return False, "Booking not found."
    if booking.get("email") != email:
        return False, "You can only modify your own booking."
    if booking.get("status") != BOOKING_STATUS_PENDING:
        return False, "Seat can only be changed while booking is PENDING."

    flight_id = str(booking.get("flight_id"))
    if _seat_taken(flight_id, new_seat_no):
        return False, "New seat is already booked (paid booking)."

    ok = update_one(_bookings_path(), "booking_id", booking_id, {"seat_no": new_seat_no})
    if ok:
        log_event("BOOKING_SEAT_CHANGED", f"booking_id={booking_id} new_seat={new_seat_no}")
        return True, "Seat updated."
    return False, "Failed to update seat."
