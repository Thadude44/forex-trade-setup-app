import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Forex Trade Setup via Polygon", layout="centered")

st.markdown("## 📈 Forex Trade Setup via Polygon")

st.markdown("""
Paste your [Polygon.io](https://polygon.io) API Key and the Forex symbol (e.g., `C:EURUSD`) to fetch market data across multiple timeframes.
""")

# Avoid duplicate element IDs by using unique keys
api_key = st.text_input("🔑 Polygon API Key", type="password", key="api_key")
symbol = st.text_input("🐱‍💻 Forex Symbol (format: C:EURUSD)", "C:EURUSD", key="symbol")

def fetch_polygon_data(ticker, multiplier, timespan, limit, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/now"
    params = {
        "adjusted": "true",
        "sort": "desc",
        "limit": limit,
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None, f"❌ Error {response.status_code}: {response.text}"
    return response.json(), None

if st.button("📊 Get Trade Setup Data"):
    if not api_key or not symbol:
        st.warning("Please enter both your API key and a Forex symbol.")
    else:
        with st.spinner("Fetching data..."):

            timeframes = {
                "🟢 Last 5 Daily Candles": (1, "day", 5),
                "🟡 Last 20 x 15-Min Candles": (15, "minute", 20),
                "🔴 Last 30 x 1-Min Candles": (1, "minute", 30),
            }

            for label, (multiplier, timespan, limit) in timeframes.items():
                st.subheader(label)
                data, error = fetch_polygon_data(symbol, multiplier, timespan, limit, api_key)
                if error:
                    st.error(error)
                else:
                    for i, bar in enumerate(data.get("results", []), 1):
                        dt = datetime.datetime.fromtimestamp(bar["t"] / 1000).strftime('%Y-%m-%d %H:%M')
                        st.write(f"{i}. 🕒 {dt} | Open: {bar['o']} | High: {bar['h']} | Low: {bar['l']} | Close: {bar['c']}")
