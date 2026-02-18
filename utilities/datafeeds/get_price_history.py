from utilites.datafeeds.yfinance_config import yf

def get_price_history(ticker_symbol : dict[str,int], total_portfolio_value):
    history_dict ={}
    history_dict["prices"] = {}
    history_dict["weights"] = {}
    history_dict["sector_map"] = {}
    history_dict["industry_map"] = {}
    for ticker in ticker_symbol:
        ticker_inf = yf.Ticker(ticker)
        price = ticker_inf.info["regularMarketPrice"]
        weightage = price*ticker_symbol[ticker]/total_portfolio_value
        price_run = ticker_inf.history(period="4mo")["Close"]
        industry = ticker_inf.info["industry"]
        sector = ticker_inf.info["sector"]
        history_dict["prices"][ticker] = price_run
        history_dict["weights"][ticker]= weightage
        history_dict["sector_map"][ticker]=sector
        history_dict["industry_map"][ticker]=industry

    return history_dict
