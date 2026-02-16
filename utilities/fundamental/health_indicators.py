def health_indicators(balance_a, income_a, info):
    debt = balance_a.loc["Total Debt"]
    equity = balance_a.loc["Stockholders Equity"]
    debt_to_equity = debt.iloc[0] / equity.iloc[0]

    ebit = income_a.loc["EBIT"]
    interest = income_a.loc["Interest Expense"]
    interest_coverage = ebit.iloc[0] / interest.iloc[0]

    current_assets = balance_a.loc["Current Assets"]
    current_liab = balance_a.loc["Current Liabilities"]
    current_ratio = current_assets.iloc[0] / current_liab.iloc[0]

    retained = balance_a.loc["Retained Earnings"]
    total_assets = balance_a.loc["Total Assets"]
    total_liab = balance_a.loc["Total Liabilities Net Minority Interest"]

    wc = current_assets - current_liab
    market_cap = info["marketCap"]

    altman_z = (
        1.2 * (wc.iloc[0] / total_assets.iloc[0]) +
        1.4 * (retained.iloc[0] / total_assets.iloc[0]) +
        3.3 * (ebit.iloc[0] / total_assets.iloc[0]) +
        0.6 * (market_cap / total_liab.iloc[0]) +
        1.0 * (income_a.loc["Total Revenue"].iloc[0] / total_assets.iloc[0])
    )

    return {
        "debt_to_equity": debt_to_equity,
        "interest_coverage": interest_coverage,
        "current_ratio": current_ratio,
        "altman_z": altman_z
    }
