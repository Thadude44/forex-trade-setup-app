from datetime import datetime, timedelta

# Generate formatted date ranges for Polygon API
today = datetime.utcnow().date()
start_daily = (today - timedelta(days=7)).isoformat()
end_daily = today.isoformat()

start_15m = (datetime.utcnow() - timedelta(hours=6)).isoformat()
end_15m = datetime.utcnow().isoformat()

start_1m = (datetime.utcnow() - timedelta(minutes=30)).isoformat()
end_1m = datetime.utcnow().isoformat()

(start_daily, end_daily, start_15m, end_15m, start_1m, end_1m)

