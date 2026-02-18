def correlation_based_profile(nifty_regime, sector_regime, stock_sector_corr):

    corr_val = stock_sector_corr.iloc[-1]

    if sector_regime == "SYSTEMIC":

        if "TRENDING_UP" in nifty_regime:
            preference = "HIGH_SECTOR_ALIGNMENT"
        elif "TRENDING_DOWN" in nifty_regime:
            preference = "DEFENSIVE_OR_LOW_BETA"
        else:
            preference = "AVOID_AGGRESSIVE_BETS"

    elif sector_regime == "ROTATION":

        if "RANGE_BOUND" in nifty_regime:
            preference = "LOW_SECTOR_DEPENDENCY"
        else:
            preference = "SELECTIVE_ALPHA"

    else:
        preference = "NEUTRAL_SELECTION"

    return {
        "stock_sector_corr": round(corr_val, 3),
        "preferred_profile": preference
    }
