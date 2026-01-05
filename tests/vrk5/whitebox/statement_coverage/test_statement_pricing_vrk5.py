from src.utils.pricing_engine import dynamic_price

def test_dynamic_price_peak_morning_increases():
    p = dynamic_price(base_price=100, date_str="2026-02-14", depart_hhmm="08:00", passengers=1)
    assert p >= 100

def test_dynamic_price_night_can_decrease_but_not_below_1():
    p = dynamic_price(base_price=5, date_str="2026-02-14", depart_hhmm="02:00", passengers=1)
    assert p >= 1

def test_dynamic_price_group_discount_applies():
    p1 = dynamic_price(base_price=200, date_str="2026-02-14", depart_hhmm="12:00", passengers=1)
    p4 = dynamic_price(base_price=200, date_str="2026-02-14", depart_hhmm="12:00", passengers=4)
    assert p4 <= p1
