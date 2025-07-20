# Streamlit App: Cleaned & Fixed Forex Trade Setup Generator
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Forex Trade Setup Generator", layout="centered")
st.title("\U0001F4C8 Forex Trade Setup via Polygon")

st.markdown("""
Paste your [Polygon.io](https://polygon.io) API Key and the Forex symbol (e.g., `C:EURUSD`) to fetch market data across multiple timeframes.
---
""")

api_key = st.text_input("\U0001F511 Polygon API Key", type="password")
symbol = st.text_input("\U0001F4B1 Forex Symbol (format: C:EURUSD)", value="C:EURUSD")
submit = st.button("\U0001F4CA Get Trade Setup Data")

@st.cache_data(ttl=60)
def fetch_candles(symbol, timespan, limit):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timespan}/now?adjusted=true&sort=desc&limit={limit}&apiKey={api_key}"
    res = requests.get(url)
    try:
        res.raise_for_status()
        return res.json().get("results", [])
    except Exception as e:
        st.error(f"Error fetching {timespan} data: {e}")
        return []

def format_candles(raw):
    return [
        {
            "timestamp": pd.to_datetime(candle["t"], unit="ms").strftime("%Y-%m-%d %H:%M"),
            "open": candle["o"],
            "high": candle["h"],
            "low": candle["l"],
            "close": candle["c"]
        } for candle in raw
    ]

if submit and api_key and symbol:
    with st.spinner("Fetching data from Polygon..."):
        # Daily candles (last 5 days)
        daily_raw = fetch_candles(symbol, "day", 5)
        daily = format_candles(daily_raw)

        # Minute candles (last 300 min, used for 15-min and 1-min)
        minute_raw = fetch_candles(symbol, "minute", 300)
        m1 = format_candles(minute_raw[-30:])
        m15 = [minute_raw[i:i+15] for i in range(0, min(len(minute_raw), 300), 15)]
        m15 = format_candles([x[-1] for x in m15][-20:])  # Take last candle in each 15-min chunk

    st.subheader("\U0001F7E2 Last 5 Daily Candles")
    st.code(daily, language="json")

    st.subheader("\U0001F7E1 Last 20 15-Minute Candles")
    st.code(m15, language="json")

    st.subheader("\U0001F534 Last 30 1-Minute Candles")
    st.code(m1, language="json")

    st.subheader("\U0001F4AC Prompt to Use in ChatGPT")
    prompt = f"""Based on the following market data:

### Daily Candles:
{daily}

### 15-Minute Candles:
{m15}

### 1-Minute Candles:
{m1}

What is the highest-probability Forex trade setup based on trend, confluence, and momentum?\nProvide direction, entry, stop loss, target, and reasoning."""

    st.text_area("Prompt to Copy", prompt, height=400)

elif submit:
    st.warning("Please enter both API Key and symbol.")
