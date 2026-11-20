


import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HOTELS_PATH = DATA_DIR / "hotels.json"


def load_hotels() -> list[dict]:
   
    try:
        with open(HOTELS_PATH, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return []


def search_hotels(
    city: str,
    min_stars: int = 1,
    max_price_per_night: int | None = None,
    sort_by: str = "price",
) -> dict:
    if sort_by not in ("price", "stars"):
        return {"error": "sort_by sirf 'price' ya 'stars' ho sakta hai"}

    all_hotels = load_hotels()
    if not all_hotels:
        return {"error": "Hotel data load nahi hua"}

    matches = [
        hotel for hotel in all_hotels
        if hotel["city"].strip().lower() == city.strip().lower()
        and hotel["stars"] >= min_stars
        and (max_price_per_night is None or hotel["price_per_night"] <= max_price_per_night)
    ]

    if not matches:
        return {"error": f"{city} mein filters ke hisaab se koi hotel nahi mila"}

    if sort_by == "price":
        matches.sort(key=lambda hotel: hotel["price_per_night"])
    else:
        matches.sort(key=lambda hotel: hotel["stars"], reverse=True)

    return {"hotels": matches}