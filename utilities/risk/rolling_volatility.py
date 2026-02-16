def rolling_volatility(returns, window=20):
    return returns.rolling(window,min_periods= 1).std()