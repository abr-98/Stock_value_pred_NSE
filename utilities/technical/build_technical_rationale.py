def build_technical_rationale(t: dict) -> str:
    """
    Deterministic rationale generator from technical indicators.

    t → output of technical_agent(df)
    """

    rationale = []

    price = t.get("price")
    ema_50 = t.get("EMA_50")
    ema_200 = t.get("EMA_200")
    rsi_val = t.get("RSI")
    macd_val = t.get("MACD_hist")
    bb_penalty = t.get("BB_penalty")
    vol_ratio = t.get("vol_ratio")

    # =====================================================
    # TREND STRUCTURE
    # =====================================================

    if ema_50 is not None and ema_200 is not None:

        if ema_50 > ema_200:
            rationale.append("EMA50 above EMA200 → Primary uptrend")

        elif ema_50 < ema_200:
            rationale.append("EMA50 below EMA200 → Primary downtrend")

        else:
            rationale.append("EMA50 ≈ EMA200 → Trend equilibrium")

    # =====================================================
    # MOMENTUM STATE
    # =====================================================

    if rsi_val is not None:

        if rsi_val > 70:
            rationale.append("RSI above 70 → Overbought regime")

        elif rsi_val < 30:
            rationale.append("RSI below 30 → Oversold regime")

        elif rsi_val > 50:
            rationale.append("RSI above 50 → Bullish momentum")

        else:
            rationale.append("RSI below 50 → Bearish momentum")

    if macd_val is not None:

        if macd_val > 0:
            rationale.append("MACD histogram positive → Momentum confirmation")

        elif macd_val < 0:
            rationale.append("MACD histogram negative → Momentum weakening")

    # =====================================================
    # BOLLINGER CONTEXT
    # =====================================================

    if bb_penalty is not None:

        if bb_penalty > 0.7:
            rationale.append("Price extended from Bollinger mid → Mean reversion risk")

        elif bb_penalty < 0.3:
            rationale.append("Price near Bollinger mid → Balanced region")

    # =====================================================
    # VOLUME PARTICIPATION
    # =====================================================

    if vol_ratio is not None:

        if vol_ratio > 1.5:
            rationale.append("High volume participation → Strong conviction")

        elif vol_ratio < 0.7:
            rationale.append("Low volume participation → Weak conviction")

    if t.get("volume_spike"):
        rationale.append("Volume spike detected → Participation surge")

    # =====================================================
    # FLOW & ACCUMULATION SIGNALS
    # =====================================================

    if t.get("vpt_trend") == 1:
        rationale.append("VPT rising → Positive volume-price flow")

    elif t.get("vpt_trend") == -1:
        rationale.append("VPT falling → Negative volume-price flow")

    if t.get("adl_trend") == 1:
        rationale.append("ADL rising → Accumulation behavior")

    elif t.get("adl_trend") == -1:
        rationale.append("ADL falling → Distribution behavior")

    # =====================================================
    # DIVERGENCE DETECTION (VERY IMPORTANT)
    # =====================================================

    if t.get("accumulation_divergence"):
        rationale.append("Accumulation divergence → Hidden buying pressure")

    if t.get("distribution_divergence"):
        rationale.append("Distribution divergence → Hidden selling pressure")

    # =====================================================
    # MOMENTUM QUALITY
    # =====================================================

    if t.get("momentum") is not None:

        if t["momentum"] > 0:
            rationale.append("Momentum positive")

        elif t["momentum"] < 0:
            rationale.append("Momentum negative")

    if t.get("adjusted_momentum") is not None:

        if abs(t["adjusted_momentum"]) < abs(t.get("momentum", 0)):
            rationale.append("Volume-adjusted momentum dampened → Participation mismatch")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("No dominant technical signals detected")

    return " | ".join(rationale)
