from utilities.datafeeds.get_ticket_history import get_ticker_history
from utilities.datafeeds.get_ticket_history_week import get_ticker_history_week
from utilities.datafeeds.get_nifty_50 import get_nifty_50
import pandas as pd

class DataFetcherStock:

    @staticmethod
    def get_stock_price(symbol) -> pd.DataFrame:
        try:
            history = get_ticker_history(symbol)
            if history.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            return history
        except Exception as e:
            raise ValueError(f"Error fetching data for symbol: {symbol}")

        
    @staticmethod
    def get_stock_price_week(symbol) -> pd.DataFrame:
        try:
            history = get_ticker_history_week(symbol)
            if history.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            return history
        except Exception as e:
            raise ValueError(f"Error fetching data for symbol: {symbol}")
        
class DataFetcherNifty50:

    @staticmethod
    def get_nifty_50_data(models):
        try:
            nifty_df, nifty_X, nifty_model = get_nifty_50(models)
            if nifty_df.empty or nifty_X is None or nifty_model is None:
                raise ValueError("No data found for Nifty 50")
            return nifty_df, nifty_X, nifty_model
        except Exception as e:
            raise ValueError("Error fetching data for Nifty 50")
