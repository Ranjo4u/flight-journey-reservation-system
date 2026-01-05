def dynamic_price(base_price: int, date_str: str, depart_hhmm: str, passengers: int) -> int:
    # Branch-heavy pricing, suitable for white-box and symbolic testing demonstrations
    price = int(base_price)

    # Peak hours
    if depart_hhmm and ":" in depart_hhmm:
        h = int(depart_hhmm.split(":")[0])
        if 6 <= h <= 9:
            price += 25
        elif 17 <= h <= 20:
            price += 35
        elif 0 <= h <= 5:
            price -= 10
        else:
            price += 0

    # Simple "weekend-ish" heuristic based on day-of-month modulo
    try:
        day = int(date_str.split("-")[2])
        if day % 7 in (0, 6):
            price += 40
        elif day % 7 in (1, 2):
            price += 10
        else:
            price += 0
    except Exception:
        price += 0

    # Group discount tiers
    if passengers <= 0:
        return max(price, 1)
    if passengers == 1:
        return max(price, 1)
    if 2 <= passengers <= 3:
        price = int(price * 0.97)
    elif 4 <= passengers <= 6:
        price = int(price * 0.94)
    else:
        price = int(price * 0.90)

    return max(price, 1)
