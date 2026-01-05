from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register
from src.services.flight_service import list_all_flights
from src.services.booking_service import create_booking, get_booking, cancel_booking
from src.services.payment_service import pay_for_booking

def test_st_pending_to_paid():
    seed_if_empty()
    register("st_paid@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("st_paid@test.com", flight_id, "A", 1, "1A")
    assert ok, msg
    bid = booking["booking_id"]
    assert get_booking(bid)["status"] == "PENDING"

    ok, msg = pay_for_booking("st_paid@test.com", bid, simulate="")
    assert ok, msg
    assert get_booking(bid)["status"] == "PAID"

def test_st_pending_to_cancelled():
    seed_if_empty()
    register("st_cancel@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("st_cancel@test.com", flight_id, "B", 1, "2B")
    assert ok, msg
    bid = booking["booking_id"]
    assert get_booking(bid)["status"] == "PENDING"

    ok, msg = cancel_booking("st_cancel@test.com", bid)
    assert ok, msg
    assert get_booking(bid)["status"] == "CANCELLED"
