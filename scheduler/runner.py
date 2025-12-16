import sys, os

# === ADD THIS FIX ===
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
# ====================

import time

from data.twelvedata_forex import get_forex_candles
from data.twelvedata_stocks import get_stock_candles
from data.twelvedata_crypto import get_crypto_candles

from bot.telegram_bot import send_signal_message
from strategy.rsi import rsi_signal

# =========================
# CONFIGURATION
# =========================

MARKETS = [
    # FOREX
    {"market": "FOREX", "symbol": "EUR/USD", "interval": "5min", "lookback": 60},
    {"market": "FOREX", "symbol": "GBP/USD", "interval": "5min", "lookback": 60},

    # STOCKS
    {"market": "STOCKS", "symbol": "AAPL", "interval": "5min", "lookback": 60},
    {"market": "STOCKS", "symbol": "TSLA", "interval": "5min", "lookback": 60},

    # CRYPTO (Twelve Data format)
    {"market": "CRYPTO", "symbol": "BTC/USD", "interval": "5min", "lookback": 60},
    {"market": "CRYPTO", "symbol": "ETH/USD", "interval": "5min", "lookback": 60},
]

INTERVAL = 300  # 5 minutes


def fetch_data(market, symbol, interval, lookback):
    if market == "FOREX":
        return get_forex_candles(
            pair=symbol,
            interval=interval,
            lookback_minutes=lookback
        )

    if market == "STOCKS":
        return get_stock_candles(
            symbol=symbol,
            interval=interval,
            lookback_minutes=lookback
        )

    if market == "CRYPTO":
        return get_crypto_candles(
            symbol=symbol,
            interval=interval,
            lookback_minutes=lookback
        )

    return []


def run_bot():
    print("🚀 Twelve Data Signal Bot Started")

    while True:
        for item in MARKETS:
            market = item["market"]
            symbol = item["symbol"]
            interval = item["interval"]
            lookback = item["lookback"]

            closes = fetch_data(market, symbol, interval, lookback)

            if not closes:
                continue

            signal = rsi_signal(closes)

            if signal:
                send_signal_message(
                    market=market,
                    pair=symbol,
                    signal=signal,
                    timeframe=interval,
                    validity="Next candle",
                    note="Educational signal – manage risk"
                )

        print(f"⏳ Sleeping for {INTERVAL} seconds...\n")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    run_bot()
