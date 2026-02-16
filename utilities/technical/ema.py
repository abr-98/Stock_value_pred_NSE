def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()