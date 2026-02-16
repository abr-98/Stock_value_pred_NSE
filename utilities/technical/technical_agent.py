from utilites.technical.ema import ema
from utilites.technical.bollinger import bollinger
from utilites.technical.rsi import rsi
from utilites.technical.macd import macd
import numpy as np


def technical_agent(df):
    """
    df must contain: ['close']
    """

    close = df["Close"]

    ema_50 = ema(close, 50).iloc[-1]
    ema_200 = ema(close, 200).iloc[-1]
    rsi_val = rsi(close).iloc[-1]
    macd_val = macd(close).iloc[-1]
    bb_upper, bb_mid, bb_lower = bollinger(close)

    price = close.iloc[-1]

    # Direction
    direction = np.sign(ema_50 - ema_200)

    # Momentum agreement
    momentum = 0.5 * np.sign(rsi_val - 50) + 0.5 * np.sign(macd_val)

    # Bollinger penalty
    band_width = bb_upper.iloc[-1] - bb_lower.iloc[-1]
    bb_penalty = abs(price - bb_mid.iloc[-1]) / band_width if band_width > 0 else 0
    bb_penalty = min(bb_penalty, 1.0)



    return {
          "EMA_50": round(ema_50, 2),
          "EMA_200": round(ema_200, 2),
          "RSI": round(rsi_val, 2),
          "MACD_hist": round(macd_val, 4),
          "BB_upper": round(bb_upper.iloc[-1], 2),
          "BB_mid": round(bb_mid.iloc[-1], 2),
          "BB_lower": round(bb_lower.iloc[-1], 2),
          "BB_penalty": round(bb_penalty, 2),
          "momentum": round(momentum, 2),
          "direction": direction,
          "price": round(price, 2)
    }
