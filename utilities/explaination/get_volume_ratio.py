def get_volume_ratio(df, window=20):
    vol_mean = df["Volume"].rolling(20, min_periods=1).mean()
    df["volume_ratio"] = df["Volume"] / vol_mean
    return df