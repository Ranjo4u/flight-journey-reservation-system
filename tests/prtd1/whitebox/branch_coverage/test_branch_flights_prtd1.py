from src.seed.seed_data import seed_if_empty
from src.services.flight_service import list_all_flights, search_flights

def test_seed_creates_flights_and_search_finds_matches():
    seed_if_empty()
    flights = list_all_flights()
    assert len(flights) >= 3

    ok, msg, results = search_flights(origin="LHR", dest="JFK", date_str="2026-02-14", airline="", max_price=999999)
    assert ok, msg
    assert len(results) >= 1
    assert results[0]["from"] == "LHR"
    assert results[0]["to"] == "JFK"
