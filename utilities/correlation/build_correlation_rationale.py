def build_market_sector_rationale(m: dict) -> str:

    rationale = []

    nifty_regime = m.get("nifty_regime")
    avg_corr = m.get("avg_sector_corr")
    sector_regime = m.get("sector_regime")

    # =====================================================
    # BROAD MARKET CONTEXT
    # =====================================================

    if nifty_regime is not None:
        rationale.append(f"Nifty regime classified as {nifty_regime}")

    # =====================================================
    # SECTOR SYNCHRONIZATION
    # =====================================================

    if avg_corr is not None:

        if avg_corr > 0.75:
            rationale.append("High average sector correlation → Market moving in unified mode")

        elif avg_corr < 0.4:
            rationale.append("Low average sector correlation → Sector dispersion / rotation regime")

        else:
            rationale.append("Moderate sector correlation → Partial synchronization")

    # =====================================================
    # SECTOR STRUCTURE
    # =====================================================

    if sector_regime is not None:
        rationale.append(f"Sector regime classified as {sector_regime}")

    # =====================================================
    # CROSS-METRIC INTERPRETATION
    # =====================================================

    if nifty_regime and avg_corr is not None:

        if nifty_regime == "trend" and avg_corr < 0.4:
            rationale.append("Trending market with weak sector alignment → Narrow leadership regime")

        if nifty_regime == "range" and avg_corr > 0.75:
            rationale.append("Range market with strong sector alignment → Broad consolidation phase")

    if not rationale:
        rationale.append("No dominant market / sector structural signals")

    return " | ".join(rationale)
