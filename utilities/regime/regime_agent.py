from utilites.regime.adx import adx
from utilites.regime.atr import atr
from utilites.serialization_helper import convert_to_serializable

def regime_agent(df):
    """
    df must contain: ['High', 'Low', 'Close']
    """

    high, low, close = df["High"], df["Low"], df["Close"]

    adx_val = adx(high, low, close).iloc[-1]
    atr_val = atr(high, low, close).iloc[-1]
    atr_pct = atr_val / close.iloc[-1]

    # Regime classification
    if adx_val > 25:
        regime = "TRENDING"
        confidence = min(adx_val / 40, 1.0)
    elif atr_pct > 0.03:
        regime = "VOLATILE"
        confidence = min(atr_pct / 0.06, 1.0)
    else:
        regime = "RANGE"
        confidence = 0.6

    result = {
            "ADX": round(adx_val, 2),
            "ATR_pct": round(atr_pct * 100, 2),
            "regime": regime,
            "confidence": round(confidence, 2)
          }
    
    # Convert all numpy/pandas types to Python native types
    return convert_to_serializable(result)
