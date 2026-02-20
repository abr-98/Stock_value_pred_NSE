def build_hierarchical_diversification_rationale(structure: dict) -> str:
    rationale = []

    # =====================================================
    # ASSET LEVEL
    # =====================================================

    asset = structure.get("asset_level", {})
    eff_assets = asset.get("effective_assets")
    avg_corr = asset.get("avg_corr")

    if eff_assets is not None:
        if eff_assets < 5:
            rationale.append("Portfolio effectively concentrated at asset level")
        elif eff_assets > 15:
            rationale.append("Portfolio exhibits broad asset-level diversification")

    if avg_corr is not None:
        if avg_corr > 0.7:
            rationale.append("Cross-asset correlation elevated → diversification impact reduced")
        elif avg_corr < 0.3:
            rationale.append("Cross-asset correlation subdued → diversification benefits strong")

    # =====================================================
    # INDUSTRY LEVEL
    # =====================================================

    industry = structure.get("industry_level", {})
    eff_industries = industry.get("effective_industries")
    intra_inter_ind = industry.get("intra_inter_corr")
    ind_var_contrib = industry.get("variance_contribution")

    if eff_industries is not None:
        if eff_industries < 3:
            rationale.append("Industry exposure concentrated")
        else:
            rationale.append("Industry exposures reasonably distributed")

    if intra_inter_ind:
        intra = intra_inter_ind.get("intra")
        inter = intra_inter_ind.get("inter")

        if intra is not None and inter is not None:
            if intra > inter:
                rationale.append("Return co-movement stronger within industries than across industries")

    if ind_var_contrib:
        max_group = max(ind_var_contrib, key=ind_var_contrib.get)
        max_contrib = ind_var_contrib[max_group]

        if max_contrib > 0.6:
            rationale.append(f"Portfolio risk primarily influenced by {max_group}")

    # =====================================================
    # SECTOR LEVEL
    # =====================================================

    sector = structure.get("sector_level", {})
    eff_sectors = sector.get("effective_sectors")
    intra_inter_sec = sector.get("intra_inter_corr")
    sec_var_contrib = sector.get("variance_contribution")

    if eff_sectors is not None:
        if eff_sectors < 3:
            rationale.append("Sector exposure concentrated")
        else:
            rationale.append("Sector exposures reasonably distributed")

    if intra_inter_sec:
        intra = intra_inter_sec.get("intra")
        inter = intra_inter_sec.get("inter")

        if intra is not None and inter is not None:
            if intra > inter:
                rationale.append("Return co-movement stronger within sectors than across sectors")

    if sec_var_contrib:
        max_group = max(sec_var_contrib, key=sec_var_contrib.get)
        max_contrib = sec_var_contrib[max_group]

        if max_contrib > 0.6:
            rationale.append(f"Sector-level risk influence dominated by {max_group}")

    # =====================================================
    # INDUSTRY DOMINANCE
    # =====================================================

    dominance_info = sector.get("industry_dominance")

    if dominance_info:
        dom = dominance_info.get("dominance")
        dom_industry = dominance_info.get("dominant_industry")

        if dom is not None:
            if dom > 0.6:
                rationale.append(f"Strong common factor influence detected from {dom_industry}")
            elif dom > 0.4:
                rationale.append(f"Moderate common industry factor influence ({dom_industry})")

    # =====================================================
    # CROSS-LAYER RELATIONSHIP
    # =====================================================

    if eff_industries is not None and eff_sectors is not None:
        if eff_industries < eff_sectors:
            rationale.append("Industry diversification narrower than sector diversification")

    # =====================================================
    # DEFAULT CASE
    # =====================================================

    if not rationale:
        rationale.append("Diversification structure appears balanced across hierarchy")

    return " | ".join(rationale)
