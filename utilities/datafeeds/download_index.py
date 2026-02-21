from utilities.datafeeds.yfinance_config import yf
import pandas as pd

def download_index(symbol, start="2023-01-01"):
    data = yf.download(symbol, start=start)
    return data["Close"]