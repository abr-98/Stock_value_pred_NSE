import numpy as np
import pandas as pd

def safe_div(a, b):
    return np.nan if b in [0, None, np.nan] else a / b

def cagr(series):
    series = series.dropna()
    if len(series) < 2:
        return np.nan
    n = len(series) - 1
    return (series.iloc[0] / series.iloc[-1]) ** (1 / n) - 1

def yoy_growth(series):
    return series.pct_change(-1)

def volatility(series):
    return np.nanstd(series)

def ttm(series):
    return series.iloc[:4].sum()

def avg(series, n=2):
    return series.iloc[:n].mean()