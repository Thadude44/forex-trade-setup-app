# Streamlit App: Forex Trade Setup Generator (Polygon API)
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Forex Trade Setup Generator", layout="centered")
st.title("📈 Forex Trade Setup via Polygon")

st.markdown("""
Paste your [Polygon.io](https://polygon.io) API Key and the Forex symbol (e.g., `C:EURUSD`) to fetch market data across multiple timeframes.

---
""")

api_key = st.text_input("🔑 Polygon API Key", type="password")
symbol = st.text_input("💱 Forex Symbol (format: C:EURUSD)", value="C:EURUSD")

submit = st.button("📊 Get Trade Setup Data")

@st.cache_data(ttl=60)
def fetch_candles(symbol, timespan, limit):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timespan}/now?adjusted=true&sort=desc&limit={limit}&apiKey={api_key}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []

def format_candles(raw):
    return [
        {
            "timestamp": pd.to_datetime(candle["t"], unit="ms").strftime("%Y-%m-%d %H:%M"),
            "open": candle["o"],
            "high": candle["h"],
            "low": candle["l"],
            "close": candle["c"]
        }
        for candle in raw
    ]

if submit and api_key and symbol:
    with st.spinner("Fetching data from Polygon..."):
        daily = format_candles(fetch_candles(symbol, "day", 5))
        m15 = format_candles(fetch_candles(symbol, "minute", 20*15))[-20:]  # 20 most recent 15m
        m1 = format_candles(fetch_candles(symbol, "minute", 30))

    st.subheader("🟢 Last 5 Daily Candles")
    st.code(daily, language="json")

    st.subheader("🟡 Last 20 15-Minute Candles")
    st.code(m15, language="json")

    st.subheader("🔴 Last 30 1-Minute Candles")
    st.code(m1, language="json")

    st.subheader("💬 Prompt to Use in ChatGPT")
    prompt = f"""Based on the following market data:

### Daily Candles:
{daily}

### 15-Minute Candles:
{m15}

### 1-Minute Candles:
{m1}

What is the highest-probability Forex trade setup based on trend, confluence, and momentum? Provide direction, entry, stop loss, target, and reasoning."""
    st.text_area("Prompt to Copy", prompt, height=400)

elif submit:
    st.warning("Please enter both API Key and symbol.")
