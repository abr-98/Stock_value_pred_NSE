from utilites.datafeeds.get_nifty_and_sector_data import get_nifty_and_sector_data
from utilites.datafeeds.get_stock_series import get_stock_series
from utilites.datafeeds.get_sector import get_sector_yf

class DataFetcherCorrelation:
    @staticmethod
    def fetch_correlation_data(symbol):
        try:

            sector = get_sector_yf(symbol)
            if not sector:
                raise ValueError(f"Sector information not found for symbol: {symbol}")

            
            nifty_series, sector_price_df, stock_sector_series = get_nifty_and_sector_data()
            if not nifty_series or not sector_price_df or not stock_sector_series:
                raise ValueError("No Nifty and sector data found")
            
            stock_series_data = get_stock_series(symbol)
            if not stock_series_data:
                raise ValueError("No stock series data found for the given symbols")
            
            return {
                "nifty_series": stock_series_data.get("NIFTY 50"),
                "sector_series": stock_series_data.get(f"NIFTY {sector.upper()}"),
                "sector_price_df": sector_price_df,
                "stock_sector_series": stock_series_data  # Assuming this is what you want to return
            }
        except Exception as e:
            raise ValueError(f"Error fetching correlation data: {str(e)}")