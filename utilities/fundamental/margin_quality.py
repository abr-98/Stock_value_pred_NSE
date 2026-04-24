import numpy as np
from utilities.fundamental.utility import cagr


def _safe_loc(df, key):
    """Return df.loc[key] if the key exists, else a NaN-filled Series."""
    return df.loc[key] if key in df.index else df.iloc[0] * np.nan


def margin_quality(income_a):
    revenue = _safe_loc(income_a, "Total Revenue")
    gross = _safe_loc(income_a, "Gross Profit")
    ebitda = _safe_loc(income_a, "EBITDA")
    ebit = _safe_loc(income_a, "EBIT")

    gm = gross / revenue
    ebitda_m = ebitda / revenue
    ebit_m = ebit / revenue

    return {
        "gross_margin": gm.iloc[0],
        "gross_margin_trend": cagr(gm),
        "ebitda_margin": ebitda_m.iloc[0],
        "ebit_margin_trend": cagr(ebit_m)
    }