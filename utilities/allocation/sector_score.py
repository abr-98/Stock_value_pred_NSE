from utilities.allocation.trend_strength import trend_strength

def score_sector(
    row,
    model_pred=None,
    weights=(0.4, 0.6)
):
    """
    Works for both ML and non-ML sectors
    """
    w_pred, w_trend = weights

    trend = trend_strength(row)
    #rs = relative_strength(sector_ret, nifty_ret)

    if model_pred is None:
        # fallback (no ML model)
        return w_trend * trend

    return (
        w_pred * model_pred +
        w_trend * trend
    )