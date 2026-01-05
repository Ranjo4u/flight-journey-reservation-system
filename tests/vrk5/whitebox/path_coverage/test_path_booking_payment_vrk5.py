from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register
from src.services.flight_service import list_all_flights
from src.services.booking_service import create_booking, get_booking
from src.services.payment_service import pay_for_booking

def test_create_booking_then_pay_success():
    seed_if_empty()
    register("pay@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("pay@test.com", flight_id, "John", 1, "1A")
    assert ok, msg
    assert booking is not None

    ok, msg = pay_for_booking("pay@test.com", booking["booking_id"], simulate="")
    assert ok, msg

    b2 = get_booking(booking["booking_id"])
    assert b2 is not None
    assert b2["status"] == "PAID"

def test_pay_timeout_keeps_pending():
    seed_if_empty()
    register("timeout@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, _, booking = create_booking("timeout@test.com", flight_id, "Jane", 1, "2B")
    assert ok and booking

    ok, msg = pay_for_booking("timeout@test.com", booking["booking_id"], simulate="timeout")
    assert not ok
    assert "failed" in msg.lower()

    b2 = get_booking(booking["booking_id"])
    assert b2 is not None
    assert b2["status"] == "PENDING"
