import pandas as pd

def grouped_returns(returns: pd.DataFrame, group_map):
    groups = {}
    for asset in returns.columns:
        group = group_map.get(asset, "Unknown")
        groups.setdefault(group, []).append(asset)

    return pd.DataFrame({
        group: returns[assets].mean(axis=1)
        for group, assets in groups.items()
    })