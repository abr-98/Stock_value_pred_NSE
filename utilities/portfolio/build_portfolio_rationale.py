def build_portfolio_rationale(corr: dict, risk: dict) -> str:
    """
    Unified deterministic rationale generator.

    corr → correlation / concentration diagnostics
    risk → portfolio risk surface diagnostics
    """

    rationale = []

    # =====================================================
    # EXTRACT CORRELATION STRUCTURE METRICS
    # =====================================================

    avg_corr = corr.get("avg_correlation")
    corr_trend = corr.get("avg_correlation_trend")
    enb = corr.get("effective_bets")
    var_conc = corr.get("variance_concentration").get("pc1_variance")
    corr_regime = corr.get("correlation_regime")

    # =====================================================
    # EXTRACT PORTFOLIO RISK METRICS
    # =====================================================

    vol = risk.get("annual_volatility")
    cvar = risk.get("cvar")
    div_ratio = risk.get("diversification_ratio")
    risk_score = risk.get("risk_score")
    confidence = risk.get("confidence")

    # =====================================================
    # CORRELATION LEVEL
    # =====================================================

    if avg_corr is not None:

        if avg_corr > 0.75:
            rationale.append("High average correlation → Portfolio behaving as unified risk cluster")

        elif avg_corr < 0.35:
            rationale.append("Low average correlation → Diversification structure strong")

        else:
            rationale.append("Moderate correlation environment")

    # =====================================================
    # CORRELATION TREND
    # =====================================================

    if corr_trend is not None:

        if corr_trend > 0:
            rationale.append("Correlation trend rising → Diversification deteriorating")

        elif corr_trend < 0:
            rationale.append("Correlation trend declining → Diversification improving")

    # =====================================================
    # EFFECTIVE BETS
    # =====================================================

    if enb is not None:

        if enb < 3:
            rationale.append("Low effective bets → Concentration risk elevated")

        elif enb > 10:
            rationale.append("High effective bets → Risk well distributed")

    # =====================================================
    # VARIANCE CONCENTRATION
    # =====================================================

    if var_conc is not None and var_conc > 0.4:
        rationale.append("Variance concentration high → Risk dominated by few assets")

    # =====================================================
    # CORRELATION REGIME
    # =====================================================

    if corr_regime is not None:
        rationale.append(f"Correlation regime classified as {corr_regime}")

    # =====================================================
    # VOLATILITY STATE
    # =====================================================

    if vol is not None:

        if vol > 0.30:
            rationale.append("Annual volatility elevated → Portfolio instability high")

        elif vol < 0.12:
            rationale.append("Annual volatility subdued → Return variability contained")

    # =====================================================
    # TAIL RISK
    # =====================================================

    if cvar is not None:

        if cvar > 8:
            rationale.append("Tail risk significant → Extreme loss exposure elevated")

        elif cvar < 3:
            rationale.append("Tail risk limited → Downside shocks historically muted")

    # =====================================================
    # DIVERSIFICATION EFFICIENCY
    # =====================================================

    if div_ratio is not None:

        if div_ratio > 1.5:
            rationale.append("Diversification ratio strong → Efficient risk spreading")

        elif div_ratio < 1.1:
            rationale.append("Diversification ratio weak → Inefficient diversification")

    # =====================================================
    # AGGREGATE RISK POSTURE
    # =====================================================

    if risk_score is not None:

        if risk_score > 70:
            rationale.append("Risk score elevated → Portfolio risk posture aggressive")

        elif risk_score < 30:
            rationale.append("Risk score low → Portfolio risk posture defensive")

    # =====================================================
    # CROSS-METRIC INTERPRETATIONS (VERY IMPORTANT)
    # =====================================================

    if avg_corr is not None and enb is not None:

        if avg_corr > 0.75 and enb < 3:
            rationale.append("Highly correlated & concentrated → Portfolio fragility high")

    if vol is not None and cvar is not None:

        if vol > 0.30 and cvar > 8:
            rationale.append("High volatility & tail risk → Downside risk regime unstable")

    # =====================================================
    # CONFIDENCE INTERPRETATION
    # =====================================================

    if confidence is not None:

        if confidence > 0.75:
            rationale.append("Risk diagnostics confidence high")

        elif confidence < 0.4:
            rationale.append("Risk diagnostics confidence low → Interpret cautiously")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("Portfolio risk & correlation metrics within normal bounds")

    return " | ".join(rationale)
