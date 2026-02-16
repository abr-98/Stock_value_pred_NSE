def market_is_bullish(nifty_row, nifty_pred):
    """
    Hard gate: decides risk ON / OFF
    """
    return (
        nifty_pred > 0 and
        nifty_row["EMA_50"] > nifty_row["EMA_200"] and
        nifty_row["ADX"] > 20
    )