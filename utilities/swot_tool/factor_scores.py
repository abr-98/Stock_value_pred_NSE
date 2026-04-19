def factor_scores(df):
    df["quality"] = (df["roe_pct"] + df["margin_pct"]) / 2
    df["growth"] = df["rev_growth_pct"]
    df["valuation"] = df["pe_pct"]
    df["leverage"] = df["debt_equity_pct"]

    return df