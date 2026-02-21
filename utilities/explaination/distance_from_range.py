def distance_from_range_series(df, window=30):

    rolling_high = df["High"].rolling(window, min_periods=1).max()
    rolling_low = df["Low"].rolling(window, min_periods=1).min()

    range_width = rolling_high - rolling_low

    dist = (df["Close"] - rolling_low) / range_width

    return dist