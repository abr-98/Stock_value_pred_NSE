import numpy as np


def _safe_loc(df, key):
    return df.loc[key] if key in df.index else df.iloc[0] * np.nan


def _first(series):
    if series is None or len(series) == 0:
        return np.nan
    return series.iloc[0]


def _safe_div(a, b):
    if b in [0, None] or (isinstance(b, float) and np.isnan(b)):
        return np.nan
    if isinstance(a, float) and np.isnan(a):
        return np.nan
    return a / b


def _is_bfsi(info):
    sector = str((info or {}).get("sector", "")).lower()
    industry = str((info or {}).get("industry", "")).lower()
    text = f"{sector} {industry}"
    return any(k in text for k in ["bank", "financial", "insurance", "nbfc"])


def _best_effort_ebit(income_a, info):
    ebit = _safe_loc(income_a, "EBIT")
    if not np.isnan(_first(ebit)):
        return ebit

    # Banking/financial statements often omit EBIT; use operating/pretax proxy if available.
    for key in ["Operating Income", "Pretax Income"]:
        proxy = _safe_loc(income_a, key)
        if not np.isnan(_first(proxy)):
            return proxy

    if _is_bfsi(info):
        return income_a.iloc[0] * np.nan

    return ebit


def health_indicators(balance_a, income_a, info):
    debt = _safe_loc(balance_a, "Total Debt")
    equity = _safe_loc(balance_a, "Stockholders Equity")
    debt_to_equity = _safe_div(_first(debt), _first(equity))

    ebit = _best_effort_ebit(income_a, info)
    interest = _safe_loc(income_a, "Interest Expense")
    interest_coverage = _safe_div(_first(ebit), _first(interest))

    current_assets = _safe_loc(balance_a, "Current Assets")
    current_liab = _safe_loc(balance_a, "Current Liabilities")
    current_ratio = _safe_div(_first(current_assets), _first(current_liab))

    retained = _safe_loc(balance_a, "Retained Earnings")
    total_assets = _safe_loc(balance_a, "Total Assets")
    total_liab = _safe_loc(balance_a, "Total Liabilities Net Minority Interest")
    revenue = _safe_loc(income_a, "Total Revenue")

    wc = current_assets - current_liab
    market_cap = (info or {}).get("marketCap", np.nan)
    total_assets_0 = _first(total_assets)

    altman_z = np.nan
    if not np.isnan(total_assets_0):
        altman_z = (
            1.2 * _safe_div(_first(wc), total_assets_0) +
            1.4 * _safe_div(_first(retained), total_assets_0) +
            3.3 * _safe_div(_first(ebit), total_assets_0) +
            0.6 * _safe_div(market_cap, _first(total_liab)) +
            1.0 * _safe_div(_first(revenue), total_assets_0)
        )

    return {
        "debt_to_equity": debt_to_equity,
        "interest_coverage": interest_coverage,
        "current_ratio": current_ratio,
        "altman_z": altman_z
    }
