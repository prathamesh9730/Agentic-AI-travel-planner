# Agentic AI Travel Planner

Ek AI travel planner jo flights, hotels, attractions, weather, aur budget ko jodkar ek trip itinerary banata hai. Ye LangChain-style tool calling agent ka use karta hai, jo Groq ke LLM se chalta hai.

## website hosting using streamlit app 
## Live APP  `https://agenticai-travel-planner.streamlit.app` 


## Features

- **Flight search:** source aur destination ke hisaab se flights, price ya duration se sorted
- **Hotel search:** city, stars, aur price ke filter ke saath
- **Places discovery:** city aur type (beach, fort, temple, etc.) ke hisaab se attractions
- **Weather forecast:** Open-Meteo API se roz ka max temperature (bina API key ke)
- **Budget estimate:** flight + hotel + daily expenses ka total
- **Streamlit UI:** valid routes dropdown ke saath trip form

## Project structure

```
Travel_Planner/
├── app.py                  # Streamlit app
├── test_agent.py           # Agent ka test
├── requirements.txt
├── .env                    # API key (GitHub par nahi)
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
└── tools_agent/
    ├── __init__.py
    ├── agent.py            # LLM + tool calling loop
    ├── flight_tool.py
    ├── hotel_tool.py
    ├── places_tool.py
    ├── weather_tool.py
    └── budget_tool.py
```

## Setup

1. Repository clone ya download kariye.
2. Dependencies install kariye:
   ```bash
   pip install -r requirements.txt
   ```
3. Groq se free API key lijiye ([console.groq.com](https://console.groq.com)).
4. Project folder mein `.env` file banaiye, aur ye likhiye:
   ```
   GROQ_API_KEY=your_key_here
   ```

## Run karein

App chalane ke liye:

```bash
streamlit run app.py
```

Browser mein `http://localhost:8501` kholiye, source aur destination chuniye, aur **Plan my trip** dabaiye.

Agent test karne ke liye:

```bash
python test_agent.py
```

## Agent kaise kaam karta hai

1. User ki query LLM ko jaati hai, saath mein system prompt jisme strict rules hain.
2. LLM tool call maangta hai (jaise flight search), code tool chalata hai, aur result LLM ko wapas bhejta hai.
3. Ye loop tab tak chalta hai jab LLM final itinerary likh de.
4. Rules ke hisaab se LLM sirf tool ke data se jawab deta hai, aur data na mile to "Not found in the data" likhta hai.

## Limitations

- **Sample data:** flights, hotels, places sample JSON files se aate hain, real market ke nahi.
- **Limited routes:** sirf woh routes chalte hain jo flight data mein hain.
- **Places:** data mein kuch cities mein sirf ek type ki place hai (jaise Mumbai mein sirf beach), isliye itinerary repeat ho sakti hai.
- **Flight dates:** data ki flights 2025 ki hain, lekin weather 2026 ka forecast deta hai.
- **LLM:** prompt rules ke bawajood, model kabhi-kabhi data se bahar kuch likh sakta hai.

## Tech stack

Python, LangChain (tool calling), Groq LLM, Streamlit, Open-Meteo API.
