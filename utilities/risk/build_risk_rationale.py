def build_risk_rationale(r: dict) -> str:
    """
    Deterministic rationale generator for risk diagnostics.

    r → output of your risk / volatility MCP
    """

    rationale = []

    atr = r.get("ATR_pct")
    vol = r.get("volatility")
    dd = r.get("max_drawdown")
    cvar = r.get("cvar")

    # =====================================================
    # SHORT-TERM INSTABILITY (ATR)
    # =====================================================

    if atr is not None:

        if atr > 5:
            rationale.append("High ATR% → Elevated short-term price instability")

        elif atr < 1.5:
            rationale.append("Low ATR% → Price behavior relatively stable")

    # =====================================================
    # RETURN DISPERSION (VOLATILITY)
    # =====================================================

    if vol is not None:

        if vol > 35:
            rationale.append("High volatility → Wide return dispersion")

        elif vol < 15:
            rationale.append("Low volatility → Compressed price variability")

    # =====================================================
    # DRAWDOWN PROFILE (VERY IMPORTANT)
    # =====================================================

    if dd is not None:

        if dd > 40:
            rationale.append("Deep historical drawdowns → Severe downside episodes observed")

        elif dd < 15:
            rationale.append("Shallow drawdowns → Historical downside contained")

    # =====================================================
    # TAIL RISK (CVaR)
    # =====================================================

    if cvar is not None:

        if cvar > 10:
            rationale.append("High CVaR → Tail risk exposure significant")

        elif cvar < 3:
            rationale.append("Low CVaR → Tail losses historically limited")

    # =====================================================
    # CROSS-METRIC INTERPRETATION (NO NEW LOGIC)
    # =====================================================

    if atr is not None and vol is not None:

        if atr > 5 and vol > 35:
            rationale.append("High ATR & volatility → Unstable price regime")

    if dd is not None and cvar is not None:

        if dd > 40 and cvar > 10:
            rationale.append("Large drawdowns with heavy tails → Downside risk structurally high")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("Risk metrics within normal bounds")

    return " | ".join(rationale)
