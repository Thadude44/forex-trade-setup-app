import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Forex Trade Setup via Polygon", layout="centered")
st.markdown("## 📈 Forex Trade Setup via Polygon")

st.markdown("""
Paste your [Polygon.io](https://polygon.io) API Key and a **Forex symbol** (e.g., `C:EURUSD`) to get the most recent daily candle data.
""")

api_key = st.text_input("🔑 Polygon API Key", type="password", key="api_key_input")
symbol = st.text_input("💱 Forex Symbol (e.g., C:EURUSD)", "C:EURUSD", key="symbol_input")

def fetch_prev_day_data(symbol, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"
    params = {
        "adjusted": "true",
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None, f"❌ Error {response.status_code}: {response.text}"
    return response.json(), None

if st.button("📊 Get Forex Candle"):
    if not api_key or not symbol:
        st.warning("Please enter both your API key and Forex symbol (C:XXXYYY).")
    else:
        st.subheader("🟢 Latest Daily Candle")
        data, error = fetch_prev_day_data(symbol, api_key)
        if error:
            st.error(error)
        else:
            result = data.get("results", [{}])[0]
            if result:
                dt = datetime.datetime.fromtimestamp(result["t"] / 1000).strftime('%Y-%m-%d')
                st.write(f"📆 {dt}")
                st.write(f"🔹 Open: {result['o']}")
                st.write(f"🔸 High: {result['h']}")
                st.write(f"🔻 Low: {result['l']}")
                st.write(f"🔺 Close: {result['c']}")
                st.write(f"📊 Volume: {result['v']}")
            else:
                st.warning("No candle data returned.")

