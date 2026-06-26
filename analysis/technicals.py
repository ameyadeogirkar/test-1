import pandas as pd
import numpy as np

def calculate_indicators(close):

    sma50 = close.rolling(50).mean()

    sma200 = close.rolling(200).mean()

    delta = close.diff()

    gain = (
        delta.where(delta > 0, 0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta.where(delta < 0, 0)
        .rolling(14)
        .mean()
    )

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12).mean()

    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26

    signal = macd.ewm(span=9).mean()

    return {
        "sma50": sma50,
        "sma200": sma200,
        "rsi": rsi,
        "macd": macd,
        "signal": signal
    }


def technical_score(
        current_price,
        indicators):

    score = 0

    if indicators["rsi"].iloc[-1] < 35:
        score += 1

    if (
        indicators["macd"].iloc[-1]
        >
        indicators["signal"].iloc[-1]
    ):
        score += 1

    if (
        current_price
        >
        indicators["sma200"].iloc[-1]
    ):
        score += 1

    return score