import random
from src.seed.seed_data import seed_if_empty
from src.services.flight_service import list_all_flights, search_flights

def test_random_search_does_not_crash():
    seed_if_empty()
    flights = list_all_flights()
    assert flights

    sample = random.sample(flights, k=min(10, len(flights)))
    for f in sample:
        ok, msg, results = search_flights(f["from"], f["to"], f["date"], airline="", max_price=999999)
        assert ok, msg
        assert isinstance(results, list)
