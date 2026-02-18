from utilites.datafeeds.yfinance_config import yf

def get_stock_series(symbol):
    stock_series = yf.download(symbol, start="2023-01-01")["Close"]
    return stock_series