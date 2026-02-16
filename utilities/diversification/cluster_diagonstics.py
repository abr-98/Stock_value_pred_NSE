def clustering_diagnostics(metrics):
    flags = []

    if metrics["effective_industries"] < metrics["effective_sectors"]:
        flags.append("industry_concentration")

    if metrics["industry_intra_corr"] > metrics["sector_intra_corr"]:
        flags.append("industry_herding")

    if metrics["industry_pc1"] > 0.4:
        flags.append("industry_dominated")

    return flags