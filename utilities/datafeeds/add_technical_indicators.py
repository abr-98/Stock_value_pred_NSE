from utilities.technical.rsi import rsi
from utilities.technical.macd import macd
from utilities.technical.bollinger import bollinger
from utilities.technical.ema import ema


def add_technical_indicators(df):
    df["RSI"] = rsi(df["Close"])
    df["MACD"] = macd(df["Close"])
    df["Upper"], df["Mid"], df["Lower"] = bollinger(df["Close"])
    df["EMA_50"] = ema(df["Close"], 50)
    df["EMA_200"] = ema(df["Close"], 200)
    #df_technical = df[["RSI", "MACD", "Upper","Mid","Lower","EMA_50","EMA_200"]]
    return df
