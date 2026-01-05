from pathlib import Path
import pytest

@pytest.fixture(autouse=True)
def _clean_data_files():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    for fn in ["users.jsonl", "flights.jsonl", "bookings.jsonl", "payments.jsonl", "audit.log"]:
        (data_dir / fn).write_text("", encoding="utf-8")
    yield
