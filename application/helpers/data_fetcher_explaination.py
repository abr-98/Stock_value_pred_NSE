from utilities.datafeeds.get_value import get_value


class DataFetcherExplaination:

    @staticmethod
    def fetch_symbol_value(symbol):
        try:
            data = get_value(symbol)
            if data is None:
                raise ValueError(f"Failed to fetch value for {symbol}")
            return data
        except Exception as e:
            raise ValueError(f"Error fetching value for {symbol}: {str(e)}")
