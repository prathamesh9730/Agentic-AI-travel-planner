"""Travel planning agent: Groq LLM ko tools dekar trip plan banwata hai."""

import json

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from tools_agent.budget_tool import calculate_budget
from tools_agent.flight_tool import search_flights
from tools_agent.hotel_tool import search_hotels
from tools_agent.places_tool import search_places
from tools_agent.weather_tool import format_weather_response, get_forecast

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-120b"
MAX_AGENT_STEPS = 8
FALLBACK_ANSWER = "Model ne jawab nahi diya. Query ko thoda detail mein likh kar dobara try kariye."

# Weather API ko latitude/longitude chahiye
CITY_COORDINATES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Goa": (15.2993, 74.1240),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Jaipur": (26.9124, 75.7873),
    "Kolkata": (22.5726, 88.3639),
}

SYSTEM_PROMPT = """You are a travel planning assistant. Answer only using the data returned by the tools.

Strict rules:
1. Take every flight, hotel, place, weather, and budget value only from the tool results. Do not add anything from your own knowledge.
2. Do not mention any place, hotel, or flight that is not in the tool results.
3. Take the budget total only from the budget_estimate tool. If the flight or hotel price is not found, do not call budget_estimate, and write: "Total budget cannot be calculated because flight data was not found".
4. If no data is found, say clearly: "Not found in the data".
5. Do not call the same tool again after getting its result, unless it is necessary.
6. In the itinerary, include only activities that appear in the tool results. Do not add activities such as "local market", "water sports", or "city tour" unless they are in the tool data.
7. If the tool has no place for a given day, write: "No other place is available in the data for this day".
8. Write the answer in English, using this format:
   - Trip summary
   - Flight selected
   - Hotel recommendation
   - Day-wise itinerary (only places from the tool results)
   - Weather for each day
   - Budget breakdown (the tool's total)
   - Reasoning"""


@tool
def flight_search(source: str, destination: str, sort_by: str = "price") -> str:
    """Source se destination ki flights dhoondhta hai. sort_by 'price' ya 'duration' ho sakta hai."""
    return json.dumps(search_flights(source, destination, sort_by), ensure_ascii=False)


@tool
def hotel_search(city: str, min_stars: int = 1, max_price_per_night: int = 0, sort_by: str = "price") -> str:
    """City mein hotels dhoondhta hai. max_price_per_night 0 ho to price filter nahi lagta. sort_by 'price' ya 'stars'."""
    max_price = max_price_per_night if max_price_per_night > 0 else None
    return json.dumps(search_hotels(city, min_stars, max_price, sort_by), ensure_ascii=False)


@tool
def places_search(city: str, place_type: str = "", min_rating: float = 0.0) -> str:
    """City ke attractions dhoondhta hai. place_type khali ho to sab types. Jaise beach, temple, fort."""
    chosen_type = place_type if place_type else None
    return json.dumps(search_places(city, chosen_type, min_rating), ensure_ascii=False)


@tool
def weather_forecast(city: str) -> str:
    """City ke aane wale dinon ka max temperature forecast deta hai."""
    city_name = city.strip().title()
    if city_name not in CITY_COORDINATES:
        return json.dumps({"error": f"{city} ke coordinates nahi hain"}, ensure_ascii=False)
    latitude, longitude = CITY_COORDINATES[city_name]
    weather = format_weather_response(get_forecast(latitude, longitude))
    return json.dumps(weather, ensure_ascii=False)


@tool
def budget_estimate(flight_price: float, hotel_price_per_night: float, nights: int, daily_expense: float = 800) -> str:
    """Flight, hotel aur daily expenses jodkar trip ka total budget deta hai."""
    return json.dumps(
        calculate_budget(flight_price, hotel_price_per_night, nights, daily_expense),
        ensure_ascii=False,
    )


TOOLS = [flight_search, hotel_search, places_search, weather_forecast, budget_estimate]
TOOLS_BY_NAME = {tool_item.name: tool_item for tool_item in TOOLS}


def run_tool(call: dict) -> str:
    """Model ki tool call ko chalata hai aur result string mein deta hai."""
    tool_item = TOOLS_BY_NAME.get(call["name"])
    if tool_item is None:
        return json.dumps({"error": f"Unknown tool: {call['name']}"})
    try:
        return str(tool_item.invoke(call["args"]))
    except Exception as error:
        return json.dumps({"error": str(error)})


def plan_trip(user_request: str) -> str:
    """User ki query le kar agent loop se final itinerary wapas karta hai."""
    try:
        llm = ChatGroq(model=GROQ_MODEL, temperature=0).bind_tools(TOOLS)
        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_request)]

        for _ in range(MAX_AGENT_STEPS):
            response = llm.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                return response.content or FALLBACK_ANSWER

            for call in response.tool_calls:
                messages.append(ToolMessage(content=run_tool(call), tool_call_id=call["id"]))

        return "Agent ne limit tak jawab nahi diya. Query ko chhota karke dobara try kariye."

    except Exception as error:
        return f"Agent chal nahi paya: {error}. Check kariye ki GROQ_API_KEY .env mein sahi hai."