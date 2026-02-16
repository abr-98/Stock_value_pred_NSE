import pandas as pd

def adx(high, low, close, period=14):
    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr_val = tr.rolling(period,min_periods= 1).mean()
    plus_di = 100 * (plus_dm.rolling(period,min_periods= 1).mean() / atr_val)
    minus_di = 100 * (minus_dm.rolling(period,min_periods= 1).mean() / atr_val)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di + 1e-9)) * 100
    return dx.rolling(period,min_periods= 1).mean()