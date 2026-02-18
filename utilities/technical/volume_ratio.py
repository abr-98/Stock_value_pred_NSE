def volume_ratio(volume, period=20):
    vol_avg = volume.rolling(period, min_periods=1).mean()
    return volume / (vol_avg + 1e-9)