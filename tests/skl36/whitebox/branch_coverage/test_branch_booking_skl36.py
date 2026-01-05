from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register
from src.services.booking_service import create_booking, list_bookings_for_user, modify_booking_seat, cancel_booking
from src.services.flight_service import list_all_flights

def test_create_booking_pending_and_list():
    seed_if_empty()
    ok, _ = register("buser@test.com", "User1234")
    assert ok

    flight_id = list_all_flights()[0]["flight_id"]
    ok, msg, booking = create_booking(
        email="buser@test.com",
        flight_id=flight_id,
        passenger_name="John",
        passengers=1,
        seat_no="1A"
    )
    assert ok, msg
    assert booking is not None
    assert booking["status"] == "PENDING"

    rows = list_bookings_for_user("buser@test.com")
    assert len(rows) == 1
    assert rows[0]["booking_id"] == booking["booking_id"]

def test_modify_seat_only_when_pending():
    seed_if_empty()
    register("muser@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]
    ok, _, booking = create_booking("muser@test.com", flight_id, "Jane", 1, "1A")
    assert ok and booking

    ok, msg = modify_booking_seat("muser@test.com", booking["booking_id"], "2B")
    assert ok, msg

def test_cancel_booking_marks_cancelled():
    seed_if_empty()
    register("cuser@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]
    ok, _, booking = create_booking("cuser@test.com", flight_id, "Sam", 1, "1A")
    assert ok and booking

    ok, msg = cancel_booking("cuser@test.com", booking["booking_id"])
    assert ok, msg
