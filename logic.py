def filter_stays(stays, params):
    results = []
    destination = params.get("destination", "").strip().lower()
    stay_type = params.get("type", "All").strip()
    max_price = params.get("max_price")
    max_persons = params.get("max_persons")

    bool_filters = [
        "food_included",
        "wifi",
        "gym",
        "laundry",
        "security",
        "study_room"
    ]

    for stay in stays:
        if destination and destination not in stay["city"].lower() and destination not in stay["address"].lower() and destination not in stay["name"].lower():
            continue

        if stay_type and stay_type.lower() != "all" and stay["type"].lower() != stay_type.lower():
            continue

        if max_price is not None and stay["daily_cost"] > max_price:
            continue

        if max_persons is not None:
            if max_persons == 3 and stay["max_persons"] < 3:
                continue
            elif max_persons in (1, 2) and stay["max_persons"] != max_persons:
                continue

        passed_amenities = True
        for key in bool_filters:
            if params.get(key) is True and not stay.get(key):
                passed_amenities = False
                break
        if not passed_amenities:
            continue

        results.append(stay)

    return results


def calculate_trip_budget(stay, duration_days=7, user_budget=15000):
    duration = max(1, int(duration_days))
    accommodation_total = stay["daily_cost"] * duration
    # If food is included, daily extra snacks/coffee ~ Rs 120; otherwise ~ Rs 350/day
    daily_food_est = 120 if stay["food_included"] else 350
    food_total = daily_food_est * duration
    # Estimated local transit (metro/bus/auto) ~ Rs 150/day
    transport_total = 150 * duration

    actual_expense = accommodation_total + food_total + transport_total
    refundable_deposit = stay["deposit"]
    upfront_amount = actual_expense + refundable_deposit

    return {
        "duration_days": duration,
        "accommodation_total": accommodation_total,
        "food_total": food_total,
        "transport_total": transport_total,
        "actual_expense": actual_expense,
        "refundable_deposit": refundable_deposit,
        "upfront_amount": upfront_amount,
        "within_budget": upfront_amount <= user_budget,
        "difference": user_budget - upfront_amount
    }
