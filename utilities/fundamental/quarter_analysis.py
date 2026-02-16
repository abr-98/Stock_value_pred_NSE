from utilites.fundamental.utility import volatility

def quarterly_analysis(income_q):
    revenue = income_q.loc["Total Revenue"]
    ebitda = income_q.loc["EBITDA"]
    ni = income_q.loc["Net Income"]

    return {
        "revenue_qoq": revenue.pct_change(-1).iloc[0],
        "revenue_yoy": revenue.pct_change(-4).iloc[0],
        "ebitda_qoq": ebitda.pct_change(-1).iloc[0],
        "ni_q_volatility": volatility(ni)
    }
