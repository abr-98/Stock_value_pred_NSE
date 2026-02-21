from utilities.fundamental.utility import safe_div, ttm

def valuation_indicators(info, income_q, cashflow_q):
    price = info["currentPrice"]
    market_cap = info["marketCap"]

    eps_ttm = info["trailingEps"]
    pe = safe_div(price, eps_ttm)

    ev = info["enterpriseValue"]
    ebitda_ttm = ttm(income_q.loc["EBITDA"])
    ev_ebitda = safe_div(ev, ebitda_ttm)

    pb = info["priceToBook"]

    fcf_ttm = (
        ttm(cashflow_q.loc["Operating Cash Flow"])
        - ttm(cashflow_q.loc["Capital Expenditure"])
    )
    fcf_yield = safe_div(fcf_ttm, market_cap)

    return {
        "pe": pe,
        "ev_ebitda": ev_ebitda,
        "pb": pb,
        "fcf_yield": fcf_yield
    }