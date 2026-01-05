from src.seed.seed_data import seed_if_empty
from src.services.flight_service import list_all_flights, search_flights

def test_seed_then_list_and_search():
    seed_if_empty()
    flights = list_all_flights()
    assert len(flights) >= 50

    f0 = flights[0]
    ok, msg, results = search_flights(f0["from"], f0["to"], f0["date"], airline="", max_price=999999)
    assert ok, msg
    # might be multiple, but at least one should match
    assert any(r["flight_id"] == f0["flight_id"] for r in results)
