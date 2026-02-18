def volume_ma(volume, period=20):
    return volume.rolling(period, min_periods=1).mean()