
from utilites.technical.volume_ratio import volume_ratio


def volume_spike(volume, period=20, threshold=3.0):
    vol_ratio = volume_ratio(volume, period)
    return vol_ratio > threshold