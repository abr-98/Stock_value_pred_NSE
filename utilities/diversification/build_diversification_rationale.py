def build_hierarchical_diversification_rationale(structure: dict, flags: list[str]) -> str:
    """
    Deterministic rationale generator for hierarchical diversification diagnostics.

    structure → output of hierarchical diversification agent
    flags → clustering / concentration flags
    """

    rationale = []

    # =====================================================
    # ASSET LEVEL INTERPRETATION
    # =====================================================

    asset = structure.get("asset_level", {})
    eff_assets = asset.get("effective_assets")
    avg_corr = asset.get("avg_corr")

    if eff_assets is not None:

        if eff_assets < 5:
            rationale.append("Low effective assets → Portfolio concentration at asset level")

        elif eff_assets > 15:
            rationale.append("High effective assets → Broad asset diversification")

    if avg_corr is not None:

        if avg_corr > 0.7:
            rationale.append("High average pairwise correlation → Assets moving cohesively")

        elif avg_corr < 0.3:
            rationale.append("Low cross-asset correlation → Diversification benefits strong")

    # =====================================================
    # INDUSTRY LEVEL INTERPRETATION
    # =====================================================

    industry = structure.get("industry_level", {})
    eff_industries = industry.get("effective_industries")

    if eff_industries is not None:

        if eff_industries < 3:
            rationale.append("Low effective industries → Industry concentration risk")

        else:
            rationale.append("Industry diversification structure stable")

    # =====================================================
    # SECTOR LEVEL INTERPRETATION
    # =====================================================

    sector = structure.get("sector_level", {})
    eff_sectors = sector.get("effective_sectors")

    if eff_sectors is not None:

        if eff_sectors < 3:
            rationale.append("Low effective sectors → Sector concentration risk")

        else:
            rationale.append("Sector diversification structure stable")

    # =====================================================
    # FLAG-DRIVEN STRUCTURAL RATIONALE (CRITICAL)
    # =====================================================

    if "industry_concentration" in flags:
        rationale.append("Industry concentration detected → Risk dominated by few industries")

    if "industry_herding" in flags:
        rationale.append("Industry intra-correlation elevated → Herding behavior present")

    if "industry_dominated" in flags:
        rationale.append("Industry PC1 dominance high → Systemic industry factor driving portfolio")

    # =====================================================
    # CROSS-LAYER STRUCTURAL LOGIC (NO NEW MATH)
    # =====================================================

    if eff_industries is not None and eff_sectors is not None:

        if eff_industries < eff_sectors:
            rationale.append("Industry diversification weaker than sector diversification")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("Hierarchical diversification structure within normal bounds")

    return " | ".join(rationale)
