from src.seed.seed_data import seed_if_empty
from src.services.auth_service import register, login
from src.services.flight_service import list_all_flights, search_flights

def test_ep_register_valid_then_login_success():
    seed_if_empty()
    ok, msg = register("ep_user@test.com", "User1234")
    assert ok, msg
    ok, msg, user = login("ep_user@test.com", "User1234")
    assert ok, msg
    assert user is not None

def test_ep_register_invalid_email_rejected():
    seed_if_empty()
    ok, msg = register("bad-email", "User1234")
    assert not ok
    assert "email" in msg.lower()

def test_ep_register_weak_password_rejected():
    seed_if_empty()
    ok, msg = register("weak@test.com", "weak")
    assert not ok
    assert "password" in msg.lower()

def test_ep_search_valid_inputs_returns_ok_message():
    seed_if_empty()
    f0 = list_all_flights()[0]
    ok, msg, results = search_flights(f0["from"], f0["to"], f0["date"], airline="", max_price=999999)
    assert ok, msg
    assert isinstance(results, list)
