from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register
from src.services.flight_service import list_all_flights
from src.services.booking_service import create_booking, get_booking
from src.services.payment_service import pay_for_booking

def _make_pending_booking(email: str, seat: str):
    seed_if_empty()
    register(email, "User1234")
    flight_id = list_all_flights()[0]["flight_id"]
    ok, msg, booking = create_booking(email, flight_id, "P", 1, seat)
    assert ok, msg
    return booking["booking_id"]

def test_dt_payment_success_marks_paid():
    bid = _make_pending_booking("dt_ok@test.com", "1A")
    ok, msg = pay_for_booking("dt_ok@test.com", bid, simulate="")
    assert ok, msg
    b = get_booking(bid)
    assert b["status"] == "PAID"

def test_dt_payment_timeout_keeps_pending():
    bid = _make_pending_booking("dt_to@test.com", "2B")
    ok, _ = pay_for_booking("dt_to@test.com", bid, simulate="timeout")
    b = get_booking(bid)
    assert b["status"] == "PENDING"

def test_dt_payment_insufficient_keeps_pending():
    bid = _make_pending_booking("dt_funds@test.com", "3C")
    ok, _ = pay_for_booking("dt_funds@test.com", bid, simulate="insufficient")
    b = get_booking(bid)
    assert b["status"] == "PENDING"

def test_dt_payment_fraud_keeps_pending():
    bid = _make_pending_booking("dt_fraud@test.com", "4D")
    ok, _ = pay_for_booking("dt_fraud@test.com", bid, simulate="fraud")
    b = get_booking(bid)
    assert b["status"] == "PENDING"
