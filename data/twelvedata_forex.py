import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY")

BASE_URL = "https://api.twelvedata.com/time_series"


def get_forex_candles(pair="EURUSD", interval="5min", lookback_minutes=60):
    """
    Fetches recent Forex candle data from Twelve Data.

    Parameters:
        pair (str): Forex pair, e.g., "EURUSD"
        interval (str): Candle interval (1min, 5min, 15min, 30min, 1h, 1day)
        lookback_minutes (int): How many minutes of history to fetch

    Returns:
        List of closing prices (float)
    """
    try:
        # Calculate number of candles needed
        candles_needed = max(lookback_minutes // int(interval.replace("min", "")), 10)

        params = {
            "symbol": pair,   # <== FIXED, must be EURUSD not EUR/USD
            "interval": interval,
            "outputsize": candles_needed,
            "apikey": TWELVE_DATA_API_KEY,
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if "values" not in data:
            print(f"⚠️ No candle data returned for {pair}: {data}")
            return []

        closes = [float(candle["close"]) for candle in reversed(data["values"])]

        return closes

    except Exception as e:
        print(f"❌ Error fetching Forex data for {pair}: {e}")
        return []


# Example usage
if __name__ == "__main__":
    closes = get_forex_candles(pair="EURUSD", interval="5min", lookback_minutes=60)
    print("Recent EURUSD closes:", closes)
