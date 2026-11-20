

DEFAULT_DAILY_EXPENSE = 800  # khana aur local travel, per day (INR)


def calculate_budget(
    flight_price: float,
    hotel_price_per_night: float,
    nights: int,
    daily_expense: float = DEFAULT_DAILY_EXPENSE,
) -> dict:
   
    if nights < 1:
        return {"error": "Nights kam se kam 1 honi chahiye"}
    if min(flight_price, hotel_price_per_night, daily_expense) < 0:
        return {"error": "Price aur expenses negative nahi ho sakte"}

    hotel_total = hotel_price_per_night * nights
    daily_total = daily_expense * (nights + 1)  # trip ke din = raatein + 1
    total = flight_price + hotel_total + daily_total

    return {
        "flight": flight_price,
        "hotel": hotel_total,
        "daily_expenses": daily_total,
        "total": total,
    }