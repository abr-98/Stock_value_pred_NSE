from utilities.fundamental.utility import cagr, yoy_growth

def growth_indicators(income_a, income_q, cashflow_a):
    revenue_a = income_a.loc["Total Revenue"]
    eps_a = income_a.loc["Basic EPS"]

    revenue_cagr = cagr(revenue_a)
    eps_cagr = cagr(eps_a)

    # Quarterly acceleration
    rev_q = income_q.loc["Total Revenue"]
    rev_q_growth = yoy_growth(rev_q)

    capex = cashflow_a.loc["Capital Expenditure"]
    capex_ratio = abs(capex.iloc[0]) / revenue_a.iloc[0]

    return {
        "revenue_cagr": revenue_cagr,
        "eps_cagr": eps_cagr,
        "revenue_q_acceleration": rev_q_growth.iloc[0] - rev_q_growth.iloc[1],
        "capex_ratio": capex_ratio
    }
