from utilites.technical.ema import ema
from utilites.technical.bollinger import bollinger
from utilites.technical.rsi import rsi
from utilites.technical.macd import macd
from utilites.technical.volume_ratio import volume_ratio
from utilites.technical.volume_spike import volume_spike
from utilites.technical.volume_price_trend import vpt
from utilites.technical.accumlation_distribution_line import adl
from utilites.serialization_helper import convert_to_serializable
import numpy as np


def technical_agent(df):
    """
    df must contain: ['Close', 'High', 'Low', 'Volume']
    """

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    price = close.iloc[-1]

    # === Trend & Momentum ===
    ema_50 = ema(close, 50).iloc[-1]
    ema_200 = ema(close, 200).iloc[-1]

    rsi_val = rsi(close).iloc[-1]
    macd_val = macd(close).iloc[-1]

    bb_upper, bb_mid, bb_lower = bollinger(close)

    direction = np.sign(ema_50 - ema_200)
    momentum = 0.5 * np.sign(rsi_val - 50) + 0.5 * np.sign(macd_val)

    band_width = bb_upper.iloc[-1] - bb_lower.iloc[-1]
    bb_penalty = abs(price - bb_mid.iloc[-1]) / band_width if band_width > 0 else 0
    bb_penalty = min(bb_penalty, 1.0)

    # === Volume Intelligence ===

    vol_ratio = volume_ratio(volume).iloc[-1]
    vol_spike_flag = bool(volume_spike(volume).iloc[-1])

    vpt_series = vpt(close, volume)
    vpt_trend = np.sign(vpt_series.diff().iloc[-5:].mean())

    adl_series = adl(high, low, close, volume)
    adl_trend = np.sign(adl_series.diff().iloc[-5:].mean())

    # Detect hidden accumulation / distribution
    price_trend = np.sign(close.diff().iloc[-5:].mean())
    accumulation_divergence = bool((price_trend <= 0) and (adl_trend > 0))
    distribution_divergence = bool((price_trend >= 0) and (adl_trend < 0))

    # === Volume-Adjusted Momentum Confidence ===

    volume_confidence = min(vol_ratio, 2.0) / 2.0
    adjusted_momentum = momentum * volume_confidence

    result = {
        "EMA_50": round(ema_50, 2),
        "EMA_200": round(ema_200, 2),

        "RSI": round(rsi_val, 2),
        "MACD_hist": round(macd_val, 4),

        "BB_upper": round(bb_upper.iloc[-1], 2),
        "BB_mid": round(bb_mid.iloc[-1], 2),
        "BB_lower": round(bb_lower.iloc[-1], 2),
        "BB_penalty": round(bb_penalty, 2),

        "vol_ratio": round(vol_ratio, 2),
        "volume_spike": vol_spike_flag,

        "vpt_trend": int(vpt_trend),
        "adl_trend": int(adl_trend),

        "accumulation_divergence": accumulation_divergence,
        "distribution_divergence": distribution_divergence,

        "momentum": round(momentum, 2),
        "adjusted_momentum": round(adjusted_momentum, 2),

        "direction": int(direction),
        "price": round(price, 2)
    }
    
    # Convert all numpy/pandas types to Python native types
    return convert_to_serializable(result)
