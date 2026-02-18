def build_regime_rationale(r: dict) -> str:
    """
    Deterministic rationale generator for regime diagnostics.

    r → regime MCP output
    """

    rationale = []

    adx = r.get("ADX")
    atr = r.get("ATR_pct")
    regime = r.get("regime")
    confidence = r.get("confidence")

    # =====================================================
    # TREND STRENGTH (ADX)
    # =====================================================

    if adx is not None:

        if adx > 25:
            rationale.append("ADX elevated → Strong trend strength detected")

        elif adx < 15:
            rationale.append("ADX subdued → Weak / range-bound structure")

        else:
            rationale.append("ADX moderate → Transitional trend regime")

    # =====================================================
    # VOLATILITY STATE (ATR)
    # =====================================================

    if atr is not None:

        if atr > 4:
            rationale.append("ATR% high → Elevated price instability")

        elif atr < 1.5:
            rationale.append("ATR% low → Price behavior stable")

    # =====================================================
    # REGIME CONSISTENCY CHECK
    # =====================================================

    if regime is not None:

        rationale.append(f"Regime classified as {regime}")

        if regime == "trend" and adx is not None and adx < 20:
            rationale.append("Trend regime with weak ADX → Fragile trend structure")

        if regime == "range" and adx is not None and adx > 25:
            rationale.append("Range regime despite strong ADX → Possible regime shift")

    # =====================================================
    # CONFIDENCE INTERPRETATION
    # =====================================================

    if confidence is not None:

        if confidence > 0.75:
            rationale.append("Regime confidence high → Classification reliable")

        elif confidence < 0.4:
            rationale.append("Regime confidence low → Classification uncertain")

    # =====================================================
    # CROSS-METRIC CONTEXT
    # =====================================================

    if adx is not None and atr is not None:

        if adx > 25 and atr > 4:
            rationale.append("Strong trend with high volatility → Expansion phase behavior")

        elif adx < 15 and atr < 2:
            rationale.append("Weak trend & low volatility → Mean-reverting environment")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("No dominant regime characteristics detected")

    return " | ".join(rationale)
