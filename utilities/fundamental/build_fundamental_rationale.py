def build_fundamental_rationale(f: dict) -> str:
    """
    Deterministic rationale generator from fundamental metrics.

    f → dictionary containing already-computed MCP outputs
    """

    rationale = []

    # =====================================================
    # MARGIN HEALTH
    # =====================================================

    if f.get("gross_margin_trend") is not None and f.get("ebit_margin_trend") is not None:

        if f["gross_margin_trend"] < 0 and f["ebit_margin_trend"] < 0:
            rationale.append("Gross & EBIT margins declining → Margin pressure")

        elif f["gross_margin_trend"] > 0 and f["ebit_margin_trend"] > 0:
            rationale.append("Margins expanding → Operating leverage improving")

    # =====================================================
    # EARNINGS QUALITY
    # =====================================================

    if f.get("earnings_volatility") is not None:

        if f["earnings_volatility"] > 0.3:
            rationale.append("High earnings volatility → Earnings quality risk")

        elif f["earnings_volatility"] < 0.1:
            rationale.append("Stable earnings profile → Predictability strong")

    if f.get("negative_years") is not None:

        if f["negative_years"] > 0:
            rationale.append(f"{f['negative_years']} negative earnings periods detected")

    # =====================================================
    # GROWTH DYNAMICS
    # =====================================================

    if f.get("revenue_cagr") is not None:

        if f["revenue_cagr"] > 0.15:
            rationale.append("Strong revenue CAGR → Growth engine healthy")

        elif f["revenue_cagr"] < 0.05:
            rationale.append("Weak revenue CAGR → Growth subdued")

    if f.get("revenue_q_acceleration") is not None:

        if f["revenue_q_acceleration"] < 0:
            rationale.append("Revenue acceleration negative → Growth slowdown")

        elif f["revenue_q_acceleration"] > 0:
            rationale.append("Revenue acceleration positive → Growth inflecting")

    # =====================================================
    # BALANCE SHEET
    # =====================================================

    if f.get("debt_to_equity") is not None:

        if f["debt_to_equity"] < 0:
            rationale.append("Debt-to-equity improving → Balance sheet strengthening")

        elif f["debt_to_equity"] > 1:
            rationale.append("Elevated leverage → Balance sheet risk")

    if f.get("interest_coverage") is not None:

        if f["interest_coverage"] < 1.5:
            rationale.append("Weak interest coverage → Debt servicing risk")

    if f.get("current_ratio") is not None:

        if f["current_ratio"] < 1:
            rationale.append("Low current ratio → Liquidity stress possible")

    if f.get("altman_z") is not None:

        if f["altman_z"] < 1.8:
            rationale.append("Low Altman Z-score → Distress risk elevated")

    # =====================================================
    # VALUATION vs GROWTH (VERY IMPORTANT)
    # =====================================================

    pe = f.get("pe")
    growth = f.get("revenue_cagr")

    if pe is not None and growth is not None:

        if pe > 30 and growth > 0.15:
            rationale.append("High PE supported by strong growth → Premium justified")

        elif pe > 30 and growth <= 0.15:
            rationale.append("High PE with weak growth → Valuation risk")

        elif pe < 15 and growth > 0.15:
            rationale.append("Low PE despite strong growth → Potential undervaluation")

        elif pe < 15 and growth <= 0.05:
            rationale.append("Low PE with weak growth → Possible value trap")

    # =====================================================
    # VALUATION vs STABILITY
    # =====================================================

    if pe is not None and f.get("earnings_volatility") is not None:

        if pe > 25 and f["earnings_volatility"] > 0.3:
            rationale.append("High valuation with unstable earnings → Multiple compression risk")

    if pe is not None and f.get("revenue_q_acceleration") is not None:

        if pe > 25 and f["revenue_q_acceleration"] < 0:
            rationale.append("Growth decelerating while valuation elevated → Repricing risk")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("No major fundamental stress or anomaly signals detected")

    return " | ".join(rationale)
