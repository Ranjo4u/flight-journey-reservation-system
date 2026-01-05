from src.services.auth_service import register, login

def test_register_success_then_login_success():
    ok, msg = register("user@test.com", "User1234")
    assert ok, msg
    ok, msg, user = login("user@test.com", "User1234")
    assert ok, msg
    assert user is not None
    assert user["email"] == "user@test.com"

def test_login_lockout_after_three_failures():
    ok, _ = register("lock@test.com", "User1234")
    assert ok
    for _ in range(3):
        ok, _, _ = login("lock@test.com", "Wrong1234")
        assert not ok
    ok, msg, _ = login("lock@test.com", "User1234")
    assert not ok
    assert "locked" in msg.lower()
