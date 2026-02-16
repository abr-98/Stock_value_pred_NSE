from utilites.regime.atr import atr
from utilites.regime.adx import adx


def add_regime_indicators(df):
    df["ATR"] = atr(df["High"], df["Low"], df["Close"])
    df["ADX"] = adx(df["High"], df["Low"], df["Close"])
    #regime_indicators = df[["ATR", "ADX"]]
    return df