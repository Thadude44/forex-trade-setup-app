POLYGON_API_KEY = "YOUR_API_KEY"
symbol = "C:EURUSD"  # For example, EUR/USD Forex pair
intervals = [
    ("day", 5),      # Last 5 daily candles
    ("15minute", 20),# Last 20 15m candles
    ("minute", 30),  # Last 30 1m candles
]

def get_candles(symbol, interval, limit):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{interval}/2024-07-01/2024-07-20"
    url += f"?adjusted=true&sort=desc&limit={limit}&apiKey={POLYGON_API_KEY}"
    return requests.get(url).json()

# Example:
daily = get_candles(symbol, "day", 5)
print(daily)
```

#### **Step 2: Add this to your GitHub repo**

Upload this code as `app.py` in your GitHub repo (e.g. `yourusername/forex-trade-setup-app`).

Then go back to Streamlit and:

* Set the repo to `yourusername/forex-trade-setup-app`
* Branch: `main`
* Main file path: `app.py`

