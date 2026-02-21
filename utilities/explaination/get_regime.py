import numpy as np
from utilities.explaination.compute_trend_strength_series import compute_trend_strength_series
from utilities.explaination.distance_from_range import distance_from_range_series
from utilities.explaination.get_volume_ratio import get_volume_ratio

def get_regime(df, window=20):
    df["trend_strength"] = compute_trend_strength_series(df, window)
    df["distance_from_range"] = distance_from_range_series(df, window)
    df = get_volume_ratio(df, window)

    conditions = [
        (df["trend_strength"] > 0.5) & (df["distance_from_range"] > 0.8) & (df["volume_ratio"] > 1.5),
        (df["trend_strength"] > 0.5) & (df["distance_from_range"] < 0.2) & (df["volume_ratio"] > 1.5),
        (df["trend_strength"] < 0.5) & (df["distance_from_range"] > 0.8) & (df["volume_ratio"] < 0.5),
        (df["trend_strength"] < 0.5) & (df["distance_from_range"] < 0.2) & (df["volume_ratio"] < 0.5),
    ]

    choices = ["strong_uptrend", "strong_downtrend", "weak_uptrend", "weak_downtrend"]

    df["regime"] = np.select(conditions, choices, default="neutral")

    return df