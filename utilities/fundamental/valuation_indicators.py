import numpy as np
from utilities.fundamental.utility import safe_div, ttm


def _safe_loc(df, key):
    return df.loc[key] if key in df.index else df.iloc[0] * np.nan


def _safe_info(info, key, default=np.nan):
    val = info.get(key)
    return val if val is not None else default


def valuation_indicators(info, income_q, cashflow_q):
    price = _safe_info(info, "currentPrice")
    market_cap = _safe_info(info, "marketCap")

    eps_ttm = _safe_info(info, "trailingEps")
    pe = safe_div(price, eps_ttm)

    ev = _safe_info(info, "enterpriseValue")
    ebitda_ttm = ttm(_safe_loc(income_q, "EBITDA"))
    ev_ebitda = safe_div(ev, ebitda_ttm)

    pb = _safe_info(info, "priceToBook")

    fcf_ttm = (
        ttm(_safe_loc(cashflow_q, "Operating Cash Flow"))
        - ttm(_safe_loc(cashflow_q, "Capital Expenditure"))
    )
    fcf_yield = safe_div(fcf_ttm, market_cap)

    return {
        "pe": pe,
        "ev_ebitda": ev_ebitda,
        "pb": pb,
        "fcf_yield": fcf_yield
    }