def trend_direction(window):
    sma_fast = window["Close"].rolling(20).mean()
    sma_slow = window["Close"].rolling(50).mean()

    return sma_fast.iloc[-1] > sma_slow.iloc[-1]
