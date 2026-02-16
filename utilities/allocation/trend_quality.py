def trend_quality(window):
    returns = window["Close"].pct_change().dropna()
    return returns.mean() / returns.std()
