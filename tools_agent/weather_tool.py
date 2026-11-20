"""Weather tool: Open-Meteo API se forecast lekar use readable format mein badalta hai."""

import requests

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 10


def get_forecast(latitude: float, longitude: float) -> dict:
    """Diye gaye location ke liye poora Open-Meteo JSON response lata hai.

    Error hone par {"error": "..."} return karta hai.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max",
        "timezone": "auto",
    }
    try:
        response = requests.get(
            OPEN_METEO_FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"error": f"Weather API call failed: {error}"}


def format_weather_response(forecast: dict) -> dict:
    
    if "error" in forecast:
        return {"error": forecast["error"]}

    try:
        location = {
            "latitude": forecast["latitude"],
            "longitude": forecast["longitude"],
            "timezone": forecast["timezone"],
            "elevation_m": forecast.get("elevation"),
        }
        dates = forecast["daily"]["time"]
        temps = forecast["daily"]["temperature_2m_max"]
    except (KeyError, TypeError):
        return {"error": "Unexpected response format from weather API"}

    if len(dates) != len(temps):
        return {"error": "Dates and temperatures count mismatch"}

    daily = [
        {"date": date, "max_temp_c": temp}
        for date, temp in zip(dates, temps)
    ]
    return {"location": location, "daily": daily}


if __name__ == "__main__":
    raw_forecast = get_forecast(15.2993, 74.1240)
    weather = format_weather_response(raw_forecast)

    if "error" in weather:
        print("no weather data found:", weather["error"])
    else:
        location = weather["location"]
        print(f"Location: lat {location['latitude']}, lon {location['longitude']}")
        print(f"Timezone: {location['timezone']}")
        print(f"Elevation: {location['elevation_m']} m")
        print()
        for day in weather["daily"]:
            print(f"{day['date']}: {day['max_temp_c']} °C")