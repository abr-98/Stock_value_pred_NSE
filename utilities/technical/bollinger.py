def bollinger(series, window=20, num_std=2):
    mid = series.rolling(window,min_periods=1).mean()
    std = series.rolling(window,min_periods=1).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return upper, mid, lower