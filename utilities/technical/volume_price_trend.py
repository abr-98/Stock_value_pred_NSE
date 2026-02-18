def vpt(close, volume):
    pct_change = close.pct_change().fillna(0)
    return (pct_change * volume).cumsum()