from src.utils.pricing_engine import dynamic_price

def test_dynamic_price_never_below_1():
    assert dynamic_price(1, "2026-02-14", "02:00", 1) >= 1

def test_dynamic_price_group_discount():
    p1 = dynamic_price(200, "2026-02-14", "12:00", 1)
    p4 = dynamic_price(200, "2026-02-14", "12:00", 4)
    assert p4 <= p1
