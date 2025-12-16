import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY")

BASE_TIME_SERIES_URL = "https://api.twelvedata.com/time_series"
BASE_QUOTE_URL = "https://api.twelvedata.com/quote"


def get_stock_candles(symbol="AAPL", interval="5min", lookback_minutes=60):
    """
    Fetch recent stock candles from Twelve Data.

    Parameters:
        symbol (str): Stock symbol (e.g. "AAPL", "TSLA")
        interval (str): Interval like "1min", "5min", "15min", "1h", "1day"
        lookback_minutes (int): Minutes of historical data

    Returns:
        List of closing prices (float)
    """
    try:
        # Calculate number of candles required
        if interval.endswith("day"):
            candles_needed = max(lookback_minutes // (24 * 60), 30)
        else:
            candles_needed = max(
                lookback_minutes // int(interval.replace("min", "")),
                10
            )

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": candles_needed,
            "apikey": TWELVE_DATA_API_KEY,
        }

        response = requests.get(BASE_TIME_SERIES_URL, params=params, timeout=10)
        data = response.json()

        if "values" not in data:
            print(f"⚠️ No stock candle data for {symbol}: {data}")
            return []

        closes = [float(candle["close"]) for candle in reversed(data["values"])]
        return closes

    except Exception as e:
        print(f"❌ Error fetching stock candles for {symbol}: {e}")
        return []


def get_stock_quote(symbol="AAPL"):
    """
    Fetch real-time stock quote from Twelve Data.

    Returns:
        Dict containing price, open, high, low, previous close, timestamp
    """
    try:
        params = {
            "symbol": symbol,
            "apikey": TWELVE_DATA_API_KEY,
        }

        response = requests.get(BASE_QUOTE_URL, params=params, timeout=10)
        data = response.json()

        if "price" not in data:
            print(f"⚠️ No stock quote for {symbol}: {data}")
            return {}

        return {
            "price": float(data.get("price")),
            "open": float(data.get("open")),
            "high": float(data.get("high")),
            "low": float(data.get("low")),
            "previous_close": float(data.get("previous_close")),
            "timestamp": data.get("timestamp"),
        }

    except Exception as e:
        print(f"❌ Error fetching stock quote for {symbol}: {e}")
        return {}


# Example usage
if __name__ == "__main__":
    closes = get_stock_candles(symbol="AAPL", interval="5min", lookback_minutes=60)
    print("Recent AAPL closes:", closes)

    quote = get_stock_quote(symbol="AAPL")
    print("AAPL real-time quote:", quote)
