def sentiment_shock(extremes, shock_level=0.8):

    return (
        extremes["max_positive"] >= shock_level
        or abs(extremes["max_negative"]) >= shock_level
    )
