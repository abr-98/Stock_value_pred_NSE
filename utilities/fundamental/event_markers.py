def derive_events(f):
    return {
        "margin_pressure": f["gross_margin_trend"] < 0 and f["ebit_margin_trend"] < 0,
        "earnings_quality_deteriorating": f["earnings_volatility"] > 0.3,
        "balance_sheet_improving": f["debt_to_equity"] < 0,
        "growth_slowdown": f["revenue_q_acceleration"] < 0
    }