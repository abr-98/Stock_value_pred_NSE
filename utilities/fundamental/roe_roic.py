import numpy as np
from utilities.fundamental.utility import volatility, cagr


def _safe_loc(df, key):
    return df.loc[key] if key in df.index else df.iloc[0] * np.nan


def _is_bfsi(balance_a, income_a):
    cols = " ".join(list(balance_a.index.astype(str)) + list(income_a.index.astype(str))).lower()
    return any(k in cols for k in ["interest income", "net interest", "policy", "premium"])

def roe_roic(balance_a, income_a):
    net_income = _safe_loc(income_a, "Net Income")
    equity = _safe_loc(balance_a, "Stockholders Equity")

    roe_series = net_income / equity
    roe_level = roe_series.iloc[0]
    roe_stability = volatility(roe_series)

    ebit = _safe_loc(income_a, "EBIT")
    if np.isnan(ebit.iloc[0]):
        # BFSI statements may not expose EBIT; fall back to best available proxy.
        for key in ["Operating Income", "Pretax Income"]:
            candidate = _safe_loc(income_a, key)
            if not np.isnan(candidate.iloc[0]):
                ebit = candidate
                break

    tax = _safe_loc(income_a, "Tax Provision")
    pretax = _safe_loc(income_a, "Pretax Income")

    tax_rate = (tax / pretax).replace([np.inf, -np.inf], np.nan)
    nopat = ebit * (1 - tax_rate)

    debt = _safe_loc(balance_a, "Total Debt")
    cash = _safe_loc(balance_a, "Cash And Cash Equivalents")
    invested_capital = equity + debt - cash

    roic_series = nopat / invested_capital

    if _is_bfsi(balance_a, income_a) and np.isnan(ebit.iloc[0]):
        roic_series = roic_series * np.nan

    return {
        "roe": roe_level,
        "roe_volatility": roe_stability,
        "roic": roic_series.iloc[0],
        "roic_trend": cagr(roic_series)
    }