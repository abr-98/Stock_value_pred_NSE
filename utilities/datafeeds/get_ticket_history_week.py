from utilities.datafeeds.yfinance_config import yf

def get_ticker_history_week(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    # Get historical data (last 1 year)
    hist = ticker.history(period="10d")
    return hist