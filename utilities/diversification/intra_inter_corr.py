import numpy as np

def intra_inter_corr(returns, group_map):
    intra, inter = [], []

    for i in returns.columns:
        for j in returns.columns:
            if i >= j:
                continue
            corr = returns[i].corr(returns[j])
            if np.isnan(corr):
                continue
            if group_map.get(i) == group_map.get(j):
                intra.append(corr)
            else:
                inter.append(corr)

    return {
        "intra": float(np.nanmean(intra)) if len(intra) > 0 else np.nan,
        "inter": float(np.nanmean(inter)) if len(inter) > 0 else np.nan,
        "intra_pair_count": len(intra),
        "inter_pair_count": len(inter)
    }