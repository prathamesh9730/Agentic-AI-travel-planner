"""Streamlit app: user se trip details leta hai aur agent se itinerary dikhata hai."""

import json
from pathlib import Path

import streamlit as st

from tools_agent.agent import plan_trip

st.set_page_config(page_title="Travel Planner", page_icon="🧳", layout="centered")

DATA_DIR = Path(__file__).resolve().parent / "data"


@st.cache_data
def load_routes() -> list[tuple[str, str]]:
    """flights.json se valid (source, destination) pairs nikalta hai."""
    with open(DATA_DIR / "flights.json", encoding="utf-8") as file:
        flights = json.load(file)
    return sorted({(flight["from"], flight["to"]) for flight in flights})


def default_index(options: list[str], preferred: str) -> int:
    """Preferred city options mein ho to uska index, warna 0."""
    return options.index(preferred) if preferred in options else 0


ROUTES = load_routes()
ROUTE_SET = set(ROUTES)
SOURCE_OPTIONS = sorted({source for source, _ in ROUTES})
DESTINATION_OPTIONS = sorted({destination for _, destination in ROUTES})

st.title("🧳 Agentic AI Travel Planner")
st.caption("Your personal trip planner, powered by AI and real travel data.")

with st.form("trip_form"):
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From (source)", SOURCE_OPTIONS, index=default_index(SOURCE_OPTIONS, "Goa"))
    with col2:
        destination = st.selectbox(
            "To (destination)", DESTINATION_OPTIONS, index=default_index(DESTINATION_OPTIONS, "Mumbai")
        )

    col3, col4 = st.columns(2)
    with col3:
        nights = st.number_input("Number of nights", min_value=1, max_value=7, value=2, step=1)
    with col4:
        budget = st.number_input("Total budget (₹)", min_value=1000, max_value=500000, value=20000, step=1000)

    preference = st.text_input("Preferences", value="beaches")
    submitted = st.form_submit_button("Plan my trip", type="primary", use_container_width=True)

if submitted:
    if source == destination:
        st.error("Source aur destination alag hone chahiye.")
    elif (source, destination) not in ROUTE_SET:
        available = sorted(to for frm, to in ROUTES if frm == source)
        st.error(
            f"{source} se {destination} ki flight data mein nahi hai. "
            f"{source} se available destinations: {', '.join(available)}"
        )
    else:
        query = (
            f"{source} se {destination}, {nights} raat ki trip, "
            f"budget {budget} rupees, {preference} pasand hain."
        )
        with st.spinner("Hold on, we are creating the best travel plan for you..."):
            result = plan_trip(query)
        st.markdown(result)