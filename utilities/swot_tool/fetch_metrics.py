def fetch_metrics(tickers):
    import yfinance as yf
    import pandas as pd
    from .compute_roe import compute_roe

    data = []

    for t in tickers:
        stock = yf.Ticker(t)
        info = stock.info

        roe = compute_roe(stock)

        data.append({
            "ticker": t,
            "roe": roe,
            "pe": info.get("trailingPE"),
            "rev_growth": info.get("revenueGrowth"),
            "debt_equity": info.get("debtToEquity"),
            "margin": info.get("profitMargins")
        })

    return pd.DataFrame(data)