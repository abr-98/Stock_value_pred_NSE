from utilites.datafeeds.yfinance_config import yf

def synthetic_basket(symbols, start="2023-01-01"):
    prices = yf.download(symbols, start=start)["Close"]
    return prices.mean(axis=1)   # equal-weight basket