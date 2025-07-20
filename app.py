import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Forex Trade Setup Generator", layout="centered")
st.title("📈 Forex Trade Setup via Polygon")

st.markdown("""
Paste your [Polygon.io](https://polygon.io) API Key and Forex symbol (e.g., `C:EURUSD`).
This tool fetches multi-timeframe data and prepares a prompt for ChatGPT to generate the highest-probability trade setup (targeting 1:1 RR within 4–12 hours).
""")

# --- User Inputs ---
api_key = st.text_input("🔑 Polygon API Key", type="password")
symbol = st.text_input("💱 Forex Symbol (format: C:EURUSD)", value="C:EURUSD")
submit = st.button("📊 Get Trade Setup")

# --- Time Range Helpers ---
now = datetime.utcnow()
start_daily = (now - timedelta(days=7)).strftime("%Y-%m-%d")
end_daily = now.strftime("%Y-%m-%d")

start_15m = (now - timedelta(hours=6)).isoformat()
end_15m = now.isoformat()

start_1m = (now - timedelta(minutes=30)).isoformat()
end_1m = now.isoformat()

# --- Data Fetch Functions ---
def fetch_candles(symbol, timespan, from_date, to_date, limit=5000):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timespan}/{from_date}/{to_date}"
    params = {
        "adjusted": "true",
        "sort": "desc",
        "limit": limit,
        "apiKey": api_key
    }
    res = requests.get(url, params=params)
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
            "close": candle["c"],
            "volume": candle.get("v", 0)
        }
        for candle in raw
    ]

# --- App Logic ---
if submit and api_key and symbol:
    with st.spinner("Fetching data from Polygon..."):
        daily_raw = fetch_candles(symbol, "day", start_daily, end_daily, limit=5)
        m15_raw = fetch_candles(symbol, "minute", start_15m, end_15m, limit=200)
        m1_raw = fetch_candles(symbol, "minute", start_1m, end_1m, limit=50)

        daily = format_candles(daily_raw)[-5:]
        m15 = format_candles(m15_raw)[-20:]
        m1 = format_candles(m1_raw)[-30:]

    # --- Display Data ---
    st.subheader("🟢 Last 5 Daily Candles")
    st.json(daily)

    st.subheader("🟡 Last 20 15-Minute Candles")
    st.json(m15)

    st.subheader("🔴 Last 30 1-Minute Candles")
    st.json(m1)

    # --- ChatGPT Prompt Output ---
    st.subheader("🧠 Copy this into ChatGPT")
    prompt = f"""You are an advanced trading assistant. Based on the following market data, identify the highest-probability Forex trade setup for the next 4 to 12 hours using a 1:1 risk-reward ratio.

### DAILY CANDLES:
{daily}

### 15-MINUTE CANDLES:
{m15}

### 1-MINUTE CANDLES:
{m1}

Instructions:
- Analyze trend, price action, and momentum.
- Provide one trade idea: BUY or SELL
- Include entry price, stop loss, take profit, and why this trade has high probability.
"""
    st.text_area("Prompt for ChatGPT", prompt, height=500)

elif submit:
    st.warning("⚠️ Please enter both API Key and symbol.")
