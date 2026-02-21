import pandas as pd
from utilities.diversification.log_returns import log_returns
from utilities.diversification.grouped_returns import grouped_returns
import numpy as np

def industry_dominance(returns: pd.DataFrame, industry_map: dict):
    industry_ret = grouped_returns(returns, industry_map).dropna()

    if industry_ret.shape[1] < 2:
        return {"dominant_industry": None, "dominance": np.nan}

    corr = industry_ret.corr()
    eigenvals, eigenvecs = np.linalg.eig(corr.values)

    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]
    eigenvecs = eigenvecs[:, idx]

    pc1 = eigenvecs[:, 0]

    dominant_idx = np.argmax(np.abs(pc1))
    dominant_industry = corr.index[dominant_idx]

    return {
        "dominant_industry": dominant_industry,
        "dominance": float(eigenvals[0] / eigenvals.sum())
    }
