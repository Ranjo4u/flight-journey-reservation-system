from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register
from src.services.flight_service import list_all_flights
from src.services.booking_service import create_booking

def test_bva_passengers_lower_boundary_1_ok():
    seed_if_empty()
    register("bva1@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("bva1@test.com", flight_id, "John", 1, "1A")
    assert ok, msg
    assert booking is not None

def test_bva_passengers_0_rejected():
    seed_if_empty()
    register("bva0@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("bva0@test.com", flight_id, "John", 0, "1A")
    assert not ok
    assert "at least 1" in msg.lower()
    assert booking is None

def test_bva_invalid_seat_rejected():
    seed_if_empty()
    register("bvas@test.com", "User1234")
    flight_id = list_all_flights()[0]["flight_id"]

    ok, msg, booking = create_booking("bvas@test.com", flight_id, "John", 1, "A1")
    assert not ok
    assert booking is None
