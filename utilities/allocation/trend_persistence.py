def trend_persistence(window):
    sma20 = window["Close"].rolling(20).mean()
    above = window["Close"] > sma20
    return above.mean()
