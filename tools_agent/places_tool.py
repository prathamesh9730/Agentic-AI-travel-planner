
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PLACES_PATH = DATA_DIR / "places.json"


def load_places() -> list[dict]:
   

    
    try:
        with open(PLACES_PATH, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return []


def search_places(city: str, place_type: str | None = None, min_rating: float = 0.0) -> dict:
   

    all_places = load_places()
    if not all_places:
        return {"error": "Places data load nahi hua"}

    matches = [
        place for place in all_places
        if place["city"].strip().lower() == city.strip().lower()
        and place["rating"] >= min_rating
        and (place_type is None or place["type"].strip().lower() == place_type.strip().lower())
    ]

    if not matches:
        return {"error": f"{city} mein filters ke hisaab se koi place nahi mili"}

    matches.sort(key=lambda place: place["rating"], reverse=True)
    return {"places": matches}