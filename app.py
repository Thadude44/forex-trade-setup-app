# forex_trade_setup_app/app.py

import streamlit as st
import requests
import datetime

# --------------------- Configuration ---------------------
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = st.secrets["POLYGON_API_KEY"] if "POLYGON_API_KEY" in st.secrets else ""

# --------------------- Helpers ---------------------------
def get_candles(symbol: str, timeframe: str, limit: int):
    now = datetime.datetime.utcnow()
    if timeframe == "day":
        from_date = (now - datetime.timedelta(days=limit+3)).strftime('%Y-%m-%d')
        to_date = now.strftime('%Y-%m-%d')
    elif timeframe == "minute":
        from_date = now.strftime('%Y-%m-%d')
        to_date = now.strftime('%Y-%m-%d')
    else:
        return []

    url = f"{BASE_URL}/{symbol}/range/1/{timeframe}/{from_date}/{to_date}?adjusted=true&sort=desc&limit={limit}&apiKey={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json().get("results", [])

# --------------------- UI -------------------------------
st.title("📈 Forex Trade Setup via Polygon")
st.markdown("Paste your [Polygon.io](https://polygon.io) API Key and the Forex symbol (e.g., `C:EURUSD`) to fetch market data across multiple timeframes.")

API_KEY = st.text_input("🔑 Polygon API Key", API_KEY, type="password")
symbol = st.text_input("🐺 Forex Symbol (format: C:EURUSD)", value="C:EURUSD")

if st.button("📊 Get Trade Setup Data"):
    try:
        daily = get_candles(symbol, "day", 5)
        m15 = get_candles(symbol, "minute", 20*15)  # 20 candles on 15-min frame = 5 hours
        m1 = get_candles(symbol, "minute", 30)      # 30 candles on 1-min frame = 30 min

        st.success("✅ Data fetched successfully!")

        st.markdown("### 🟢 Last 5 Daily Candles")
        st.write(daily)

        st.markdown("### 🟡 Last 20 15-Minute Candles")
        m15_trimmed = m15[:20] if len(m15) >= 20 else m15
        st.write(m15_trimmed)

        st.markdown("### 🔴 Last 30 1-Minute Candles")
        st.write(m1)

        st.markdown("### 💬 Prompt to Use in ChatGPT")
        st.code(f"""
Based on the following market data:

### Daily Candles:
{daily}

### 15-Minute Candles:
{m15_trimmed}

### 1-Minute Candles:
{m1}

What is the highest-probability Forex trade setup based on trend, confluence, and momentum?
Provide direction, entry, stop loss, target, and reasoning.
""", language="markdown")

    except Exception as e:
        st.error(f"Error: {e}")
# forex_trade_setup_app/app.py

import streamlit as st
import requests
import datetime

# --------------------- Configuration ---------------------
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = st.secrets["POLYGON_API_KEY"] if "POLYGON_API_KEY" in st.secrets else ""

# --------------------- Helpers ---------------------------
def get_candles(symbol: str, timeframe: str, limit: int):
    now = datetime.datetime.utcnow()
    if timeframe == "day":
        from_date = (now - datetime.timedelta(days=limit+3)).strftime('%Y-%m-%d')
        to_date = now.strftime('%Y-%m-%d')
    elif timeframe == "minute":
        from_date = now.strftime('%Y-%m-%d')
        to_date = now.strftime('%Y-%m-%d')
    else:
        return []

    url = f"{BASE_URL}/{symbol}/range/1/{timeframe}/{from_date}/{to_date}?adjusted=true&sort=desc&limit={limit}&apiKey={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json().get("results", [])

# --------------------- UI -------------------------------
st.title("📈 Forex Trade Setup via Polygon")
st.markdown("Paste your [Polygon.io](https://polygon.io) API Key and the Forex symbol (e.g., `C:EURUSD`) to fetch market data across multiple timeframes.")

API_KEY = st.text_input("🔑 Polygon API Key", API_KEY, type="password")
symbol = st.text_input("🐺 Forex Symbol (format: C:EURUSD)", value="C:EURUSD")

if st.button("📊 Get Trade Setup Data"):
    try:
        daily = get_candles(symbol, "day", 5)
        m15 = get_candles(symbol, "minute", 20*15)  # 20 candles on 15-min frame = 5 hours
        m1 = get_candles(symbol, "minute", 30)      # 30 candles on 1-min frame = 30 min

        st.success("✅ Data fetched successfully!")

        st.markdown("### 🟢 Last 5 Daily Candles")
        st.write(daily)

        st.markdown("### 🟡 Last 20 15-Minute Candles")
        m15_trimmed = m15[:20] if len(m15) >= 20 else m15
        st.write(m15_trimmed)

        st.markdown("### 🔴 Last 30 1-Minute Candles")
        st.write(m1)

        st.markdown("### 💬 Prompt to Use in ChatGPT")
        st.code(f"""
Based on the following market data:

### Daily Candles:
{daily}

### 15-Minute Candles:
{m15_trimmed}

### 1-Minute Candles:
{m1}

What is the highest-probability Forex trade setup based on trend, confluence, and momentum?
Provide direction, entry, stop loss, target, and reasoning.
""", language="markdown")

    except Exception as e:
        st.error(f"Error: {e}")
