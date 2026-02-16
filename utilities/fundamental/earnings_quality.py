from utilites.fundamental.utility import volatility, cagr, yoy_growth

def earnings_quality(income_a):
    ni = income_a.loc["Net Income"]
    ni_growth = yoy_growth(ni)

    return {
        "earnings_volatility": volatility(ni_growth),
        "earnings_cagr": cagr(ni),
        "negative_years": int((ni < 0).sum())
    }