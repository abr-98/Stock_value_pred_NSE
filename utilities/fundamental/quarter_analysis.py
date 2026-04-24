import numpy as np
from utilities.fundamental.utility import volatility


def _safe_loc(df, key):
    return df.loc[key] if key in df.index else df.iloc[0] * np.nan


def quarterly_analysis(income_q):
    revenue = _safe_loc(income_q, "Total Revenue")
    ebitda = _safe_loc(income_q, "EBITDA")
    ni = _safe_loc(income_q, "Net Income")

    return {
        "revenue_qoq": revenue.pct_change(-1).iloc[0],
        "revenue_yoy": revenue.pct_change(-4).iloc[0],
        "ebitda_qoq": ebitda.pct_change(-1).iloc[0],
        "ni_q_volatility": volatility(ni)
    }
