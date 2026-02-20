import numpy as np

def classify_nifty_regime(nifty, short_window=20, long_window=50, vol_window=20):

    returns = nifty.pct_change()

    trend = nifty.rolling(short_window).mean() - nifty.rolling(long_window).mean()
    
    # Handle both Series and DataFrame cases
    trend_value = trend.iloc[-1]
    if hasattr(trend_value, 'item'):
        trend_value = trend_value.item()
    elif hasattr(trend_value, 'values'):
        trend_value = float(trend_value.values[0])
    else:
        trend_value = float(trend_value)
    
    trend_signal = np.sign(trend_value)

    vol_series = returns.rolling(vol_window).std()
    volatility_value = vol_series.iloc[-1]
    if hasattr(volatility_value, 'item'):
        volatility = volatility_value.item()
    elif hasattr(volatility_value, 'values'):
        volatility = float(volatility_value.values[0])
    else:
        volatility = float(volatility_value)

    # Calculate baseline volatility
    baseline_vol_series = returns.rolling(100, min_periods=1).std().mean()
    if hasattr(baseline_vol_series, 'item'):
        baseline_vol = baseline_vol_series.item()
    elif hasattr(baseline_vol_series, 'values'):
        baseline_vol = float(baseline_vol_series.values[0])
    else:
        baseline_vol = float(baseline_vol_series)

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
