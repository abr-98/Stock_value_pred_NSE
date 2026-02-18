import numpy as np

def classify_nifty_regime(nifty, short_window=20, long_window=50, vol_window=20):

    returns = nifty.pct_change()

    trend = nifty.rolling(short_window).mean() - nifty.rolling(long_window).mean()
    trend_signal = np.sign(float(trend.iloc[-1]))

    volatility = float(returns.rolling(vol_window).std().iloc[-1])

    baseline_vol = float(
        returns.rolling(100, min_periods=1)
               .std()
               .mean()
               .iloc[-1]
    )

    if volatility > baseline_vol:
        vol_state = "HIGH_VOL"
    else:
        vol_state = "NORMAL_VOL"

    if trend_signal > 0:
        return "TRENDING_UP_" + vol_state
    elif trend_signal < 0:
        return "TRENDING_DOWN_" + vol_state
    else:
        return "RANGE_BOUND_" + vol_state
