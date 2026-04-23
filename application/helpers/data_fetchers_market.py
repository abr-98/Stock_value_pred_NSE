from utilities.datafeeds.prepare_feed_data import prepare_feed_data


class DataFetchersMarket:

    @staticmethod
    def fetch_market_data():
        try:
            market_data = prepare_feed_data()
            if not market_data:
                raise ValueError("No market data found")
            return market_data
        except Exception as e:
            raise ValueError("Error fetching market data")
        