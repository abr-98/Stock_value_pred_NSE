def compute_trend_strength_series(df, window=20):

    net_move = (df["Close"] - df["Close"].shift(window)).abs()
    total_move = df["Close"].diff().abs().rolling(window, min_periods=1).sum()

    trend_strength = net_move / total_move

    return trend_strength