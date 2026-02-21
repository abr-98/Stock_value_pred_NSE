from utilities.diversification.industry_dominance import industry_dominance
from utilities.diversification.log_returns import log_returns
from utilities.diversification.grouped_returns import grouped_returns
from utilities.diversification.grouped_variance_contribution import group_variance_contribution
from utilities.diversification.intra_inter_corr import intra_inter_corr
from utilities.diversification.aggregate_weights import aggregate_weights
import pandas as pd
import numpy as np
from utilities.diversification.hhi import effective_number


def hierarchical_diversification_agent(prices, weights, sector_map, industry_map):
    returns = pd.DataFrame({k: log_returns(v) for k, v in prices.items()}).dropna()
    cov = returns.cov()

    sector_w = aggregate_weights(weights, sector_map)
    industry_w = aggregate_weights(weights, industry_map)

    sector_ret = grouped_returns(returns, sector_map)
    industry_ret = grouped_returns(returns, industry_map)
    industry_dom = industry_dominance(returns, industry_map)

    return {
        "asset_level": {
            "effective_assets": effective_number(weights),
            "avg_corr": returns.corr().values[np.triu_indices_from(returns.corr(), 1)].mean()
        },
        "industry_level": {
            "weights": industry_w,
            "effective_industries": effective_number(industry_w),
            "intra_inter_corr": intra_inter_corr(returns, industry_map),
            "variance_contribution": group_variance_contribution(weights, cov, industry_map),
            "industry_returns": industry_ret
        },
        "sector_level": {
            "weights": sector_w,
            "effective_sectors": effective_number(sector_w),
            "intra_inter_corr": intra_inter_corr(returns, sector_map),
            "variance_contribution": group_variance_contribution(weights, cov, sector_map),
            "sector_returns": sector_ret,
            "industry_dominance": industry_dom
        }
    }