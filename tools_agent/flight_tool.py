

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FLIGHTS_PATH = DATA_DIR / "flights.json"


def load_flights() -> list[dict]:

   
    try:
        with open(FLIGHTS_PATH, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return []


def calculate_duration_hours(flight: dict) -> float:
   
    departure = datetime.fromisoformat(flight["departure_time"])
    arrival = datetime.fromisoformat(flight["arrival_time"])
    return (arrival - departure).total_seconds() / 3600


def search_flights(source: str, destination: str, sort_by: str = "price") -> dict:
    
    

    if sort_by not in ("price", "duration"):
        return {"error": "sort_by sirf 'price' ya 'duration' ho sakta hai"}

    all_flights = load_flights()
    if not all_flights:
        return {"error": "Flight data load nahi hua"}

    matches = [
        flight for flight in all_flights
        if flight["from"].strip().lower() == source.strip().lower()
        and flight["to"].strip().lower() == destination.strip().lower()
    ]

    if not matches:
        return {"error": f"{source} se {destination} ke liye koi flight nahi mili"}

    for flight in matches:
        flight["duration_hours"] = round(calculate_duration_hours(flight), 2)

    if sort_by == "price":
        matches.sort(key=lambda flight: flight["price"])
    else:
        matches.sort(key=lambda flight: flight["duration_hours"])

    return {"flights": matches}


if __name__ == "__main__":
    result = search_flights("Goa", "Mumbai", sort_by="price")

    if "error" in result:
        print("Error:", result["error"])
    else:
        for flight in result["flights"]:
            print(
                f"{flight['airline']} | ₹{flight['price']} | "
                f"{flight['departure_time']} → {flight['arrival_time']} | "
                f"{flight['duration_hours']} hrs"
            )