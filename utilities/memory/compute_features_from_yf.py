import yfinance as yf
import pandas as pd
import numpy as np

def compute_features_from_yf(df: pd.DataFrame):

    x = pd.DataFrame()
    x["price"] = df["Close"]
    x["volume"] = df["Volume"]

    # Log returns
    x["r_1"] = np.log(x.price / x.price.shift(1))
    x["r_5"] = np.log(x.price / x.price.shift(5))
    x["r_20"] = np.log(x.price / x.price.shift(20))

    # Volatility (interpretable)
    x["vol_20"] = x["r_1"].rolling(20, min_periods=1).std()

    # Drawdown structure
    rolling_max = x.price.rolling(20, min_periods=1).max()
    x["drawdown_20"] = x.price / rolling_max - 1

    # Volume shock detection
    vol_mean = x.volume.rolling(20, min_periods=1).mean()
    vol_std = x.volume.rolling(20, min_periods=1).std()
    x["volume_z"] = (x.volume - vol_mean) / vol_std

    return x.dropna()
