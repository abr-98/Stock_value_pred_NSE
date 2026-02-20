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

            
            nifty_series, sector_price_df, stock_sector_series = get_nifty_and_sector_data(f"NIFTY {sector.upper()}")
            if nifty_series is None or sector_price_df is None or stock_sector_series is None:
                raise ValueError("No Nifty and sector data found")
            
            if nifty_series.empty or sector_price_df.empty or stock_sector_series.empty:
                raise ValueError("Nifty and sector data is empty")
            
            stock_series_data = get_stock_series(symbol)
            if stock_series_data is None or stock_series_data.empty:
                raise ValueError("No stock series data found for the given symbols")
            
            return {
                "nifty_series": nifty_series,
                "sector_price_df": sector_price_df,
                "stock_series": stock_series_data,
                "stock_sector_series": stock_sector_series
            }
        except Exception as e:
            raise ValueError(f"Error fetching correlation data: {str(e)}")