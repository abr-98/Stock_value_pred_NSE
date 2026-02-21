from utilities.allocation.trend_strength import trend_strength

def score_defensive_asset(row, nifty_trend):
    """
    Gold / Silver behave inversely in risk-off
    """
    score = trend_strength(row)

    if not nifty_trend:
        score += 1.0  # hedge boost

    return score