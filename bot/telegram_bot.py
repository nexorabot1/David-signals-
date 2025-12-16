import os
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_signal_message(market, pair, signal, timeframe, validity, note):
    """
    Sends a formatted binary trading signal to Telegram.

    Parameters:
        market (str): Market type (FOREX, STOCKS, CRYPTO)
        pair (str): Trading pair or symbol (EUR/USD, BTC/USDT, AAPL)
        signal (dict): Signal dictionary from rsi_signal()
        timeframe (str): Timeframe (e.g., 5min)
        validity (str): Signal validity (e.g., Next candle)
        note (str): Additional notes
    """
    try:
        message = f"""
📊 *BINARY SIGNAL*
🏷 *MARKET:* {market}
💱 *PAIR:* {pair}
⏱ *TIMEFRAME:* {timeframe}

📈 *SIGNAL:* {signal['direction']}
📉 *RSI:* {signal['rsi']}
🧠 *CONDITION:* {signal['condition']}

⏳ *VALIDITY:* {validity}
⚠️ _{note}_
"""

        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="Markdown"
        )

        print(f"✅ Signal sent: {pair} - {signal['direction']}")

    except Exception as e:
        print(f"❌ Failed to send signal: {e}")


# Example test
if __name__ == "__main__":
    test_signal = {
        "direction": "BUY (CALL)",
        "rsi": 27.4,
        "condition": "RSI Oversold"
    }

    send_signal_message(
        market="FOREX",
        pair="EUR/USD",
        signal=test_signal,
        timeframe="5min",
        validity="Next candle",
        note="Educational signal – manage risk"
    )
