from utilities.diversification.portfolio_variance import portfolio_variance
import numpy as np


def group_variance_contribution(weights, cov, group_map):
    total_var = portfolio_variance(weights, cov)
    contributions = {}

    for group in set(group_map.values()):
        assets = [a for a in weights if group_map[a] == group]
        idx = [cov.index.get_loc(a) for a in assets]
        w = np.array([weights[a] for a in assets])
        sub_cov = cov.iloc[idx, idx]
        contributions[group] = (w.T @ sub_cov.values @ w) / total_var

    return contributions