import pytest
from src.services.payment_service import process_payment

@pytest.mark.parametrize(
    "amount,simulate,expected_ok,expected_reason",
    [
        (0, "", False, "AMOUNT"),
        (100, "timeout", False, "TIMEOUT"),
        (100, "insufficient", False, "FUNDS"),
        (100, "fraud", False, "FRAUD"),
        (100, "", True, ""),
    ]
)
def test_symbolic_paths_process_payment(amount, simulate, expected_ok, expected_reason):
    ok, msg, details = process_payment(amount=amount, simulate=simulate)
    assert ok == expected_ok
    if expected_ok:
        assert details.get("status") == "SUCCESS"
    else:
        assert details.get("status") == "FAILED"
        assert details.get("reason") == expected_reason
