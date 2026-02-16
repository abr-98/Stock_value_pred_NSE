import yfinance as yf

def get_ticker_history(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    # Get historical data (last 1 year)
    hist = ticker.history(period="1mo")
    return hist