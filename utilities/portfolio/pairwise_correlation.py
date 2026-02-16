import pandas as pd

def pairwise_correlation(returns: pd.DataFrame):
    corr = returns.corr()

    records = []
    for i in corr.index:
        for j in corr.columns:
            if i < j:
                records.append({
                    "asset_1": i,
                    "asset_2": j,
                    "correlation": corr.loc[i, j]
                })
    return pd.DataFrame(records)