from utilities.datafeeds.yfinance_config import yf

def get_sector_yf(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    return info.get("sector", "UNKNOWN")
