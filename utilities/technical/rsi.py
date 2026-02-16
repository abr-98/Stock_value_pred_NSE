def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period,min_periods=1).mean()
    avg_loss = loss.rolling(period,min_periods=1).mean()

    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - (100 / (1 + rs))