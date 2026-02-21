import numpy as np
from utilities.fundamental.utility import volatility, cagr

def roe_roic(balance_a, income_a):
    net_income = income_a.loc["Net Income"]
    equity = balance_a.loc["Stockholders Equity"]

    roe_series = net_income / equity
    roe_level = roe_series.iloc[0]
    roe_stability = volatility(roe_series)

    ebit = income_a.loc["EBIT"]
    tax = income_a.loc["Tax Provision"]
    pretax = income_a.loc["Pretax Income"]

    tax_rate = (tax / pretax).replace([np.inf, -np.inf], np.nan)
    nopat = ebit * (1 - tax_rate)

    debt = balance_a.loc["Total Debt"]
    cash = balance_a.loc["Cash And Cash Equivalents"]
    invested_capital = equity + debt - cash

    roic_series = nopat / invested_capital

    return {
        "roe": roe_level,
        "roe_volatility": roe_stability,
        "roic": roic_series.iloc[0],
        "roic_trend": cagr(roic_series)
    }