from utilites.allocation.compute_trend_strength_window import compute_trend_strength_window


def check_trend(df, lookback=50):
    score = compute_trend_strength_window(df, lookback)

    if score >= 3:
        return "STRONG_UPTREND"
    elif score >= 2:
        return "WEAK_UPTREND"
    elif score <= -3:
        return "STRONG_DOWNTREND"
    elif score <= -2:
        return "WEAK_DOWNTREND"
    else:
        return "RANGE"