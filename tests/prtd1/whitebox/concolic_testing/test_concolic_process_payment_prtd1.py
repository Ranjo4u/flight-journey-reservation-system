from src.services.payment_service import process_payment

def test_concolic_concrete_then_mutate_to_flip_branch():
    ok1, _, d1 = process_payment(amount=100, simulate="")
    assert ok1 is True
    assert d1["status"] == "SUCCESS"

    ok2, _, d2 = process_payment(amount=100, simulate="timeout")
    assert ok2 is False
    assert d2["status"] == "FAILED"
    assert d2["reason"] == "TIMEOUT"

    ok3, _, d3 = process_payment(amount=100, simulate="fraud")
    assert ok3 is False
    assert d3["status"] == "FAILED"
    assert d3["reason"] == "FRAUD"
