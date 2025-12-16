def calculate_rsi(prices, period=14):
    """
    Calculates the Relative Strength Index (RSI).

    Parameters:
        prices (list): List of closing prices (float)
        period (int): RSI lookback period

    Returns:
        float or None: Latest RSI value
    """
    if len(prices) < period + 1:
        return None

    gains = 0.0
    losses = 0.0

    # Initial average gain/loss
    for i in range(1, period + 1):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains += change
        else:
            losses -= change  # negative change

    avg_gain = gains / period
    avg_loss = losses / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def rsi_signal(prices, period=14, oversold=30, overbought=70):
    """
    Generates a binary trading signal based on RSI.

    Parameters:
        prices (list): List of closing prices
        period (int): RSI lookback period
        oversold (int): Oversold level (CALL)
        overbought (int): Overbought level (PUT)

    Returns:
        dict or None: Signal data or None if no signal
    """
    rsi_value = calculate_rsi(prices, period)

    if rsi_value is None:
        return None

    if rsi_value <= oversold:
        return {
            "direction": "BUY (CALL)",
            "rsi": round(rsi_value, 2),
            "condition": "RSI Oversold"
        }

    if rsi_value >= overbought:
        return {
            "direction": "SELL (PUT)",
            "rsi": round(rsi_value, 2),
            "condition": "RSI Overbought"
        }

    return None


# Example usage
if __name__ == "__main__":
    closing_prices = [
        100, 101, 102, 101, 100, 99, 98, 97,
        98, 99, 100, 101, 102, 103, 104
    ]

    signal = rsi_signal(closing_prices)

    if signal:
        print(f"RSI: {signal['rsi']}")
        print(f"Signal: {signal['direction']}")
    else:
        print("No signal")
