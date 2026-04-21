def add_percentile_scores(df):
    for col in ["roe", "rev_growth", "margin"]:
        df[col + "_pct"] = df[col].rank(pct=True)

    # inverse metrics (lower is better)
    for col in ["pe", "debt_equity"]:
        df[col + "_pct"] = 1 - df[col].rank(pct=True)

    return df