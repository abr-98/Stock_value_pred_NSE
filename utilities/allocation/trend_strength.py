def trend_strength(row, no_adx=False):
    """
    Normalized interpretable trend score ∈ [0, 1]
    """

    score = 0.0
    max_score = 0.0

    # ---- EMA Trend Component ----
    max_score += 1.0
    if row["EMA_50"] > row["EMA_200"]:
        score += 1.0

    # ---- ADX Trend Strength ----
    if not no_adx:
        max_score += 0.5
        if row["ADX"] > 25:
            score += 0.5

    # ---- RSI Momentum Filter ----
    max_score += 0.5
    if row["RSI"] > 50:
        score += 0.5

    return score / max_score if max_score > 0 else 0.0
