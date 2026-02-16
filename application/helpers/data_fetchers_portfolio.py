from utilites.datafeeds.get_price_history import get_price_history


class DataFetchersPortfolio:

    @staticmethod
    def get_portfolio_details(symbol_details, total_portfolio_value) -> dict:
        try:
            details = get_price_history(symbol_details, total_portfolio_value)
            if not details:
                raise ValueError(f"No data found for symbol details: {symbol_details}")
            return details
        except Exception as e:
            raise ValueError(f"Error fetching data for symbol details: {symbol_details}")
