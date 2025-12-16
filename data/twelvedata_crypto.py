import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY")

BASE_TIME_SERIES_URL = "https://api.twelvedata.com/time_series"
BASE_CRYPTO_SYMBOLS_URL = "https://api.twelvedata.com/cryptocurrencies"


def normalize_symbol(symbol: str) -> str:
    """
    Converts symbols like 'BTC/USDT' or 'BTC-USDT' to Twelve Data format 'BTC/USD'.
    """
    symbol = symbol.replace("-", "/")

    if "/" in symbol:
        base, quote = symbol.split("/")

        # If quote is USDT → convert to USD (Twelve Data requirement)
        if quote.upper() == "USDT":
            quote = "USD"

        return f"{base.upper()}/{quote.upper()}"

    return symbol.upper()


def get_crypto_candles(symbol="BTC/USD", interval="5min", lookback_minutes=60):
    """
    Fetches recent cryptocurrency candle data from Twelve Data.

    Parameters:
        symbol (str): Crypto symbol, e.g., "BTC/USD", "ETH/USD"
        interval (str): Candle interval
        lookback_minutes (int): How many minutes of history to fetch

    Returns:
        List of closing prices (float)
    """
    try:
        # Normalize symbol
        symbol = normalize_symbol(symbol)

        # Calculate candles needed
        if interval.endswith("day"):
            candles_needed = max(lookback_minutes // (24 * 60), 30)
        else:
            candles_needed = max(lookback_minutes // int(interval.replace("min", "")), 10)

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": candles_needed,
            "apikey": TWELVE_DATA_API_KEY,
        }

        response = requests.get(BASE_TIME_SERIES_URL, params=params, timeout=10)
        data = response.json()

        if "values" not in data:
            print(f"⚠️ No candle data returned for {symbol}: {data}")
            return []

        closes = [float(candle["close"]) for candle in reversed(data["values"])]
        return closes

    except Exception as e:
        print(f"❌ Error fetching crypto data for {symbol}: {e}")
        return []


def get_crypto_symbols():
    """
    Fetches all supported crypto trading pairs from Twelve Data.

    Returns:
        List of symbol dictionaries
    """
    try:
        params = {
            "apikey": TWELVE_DATA_API_KEY
        }

        response = requests.get(BASE_CRYPTO_SYMBOLS_URL, params=params, timeout=10)
        data = response.json()

        if "data" not in data:
            print(f"⚠️ No crypto symbols returned: {data}")
            return []

        return data["data"]

    except Exception as e:
        print(f"❌ Error fetching crypto symbols: {e}")
        return []


# Example usage
if __name__ == "__main__":
    closes = get_crypto_candles(symbol="BTC/USDT", interval="5min", lookback_minutes=60)
    print("Recent BTC/USDT closes:", closes)

    symbols = get_crypto_symbols()
    print("Crypto symbols:", [s["symbol"] for s in symbols[:10]])
