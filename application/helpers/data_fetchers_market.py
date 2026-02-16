from utilites.datafeeds.prepare_feed_data import prepare_feed_data
from utilites.datafeeds.compute_sector_memberships_nifty_100 import compute_sector_memberships_nifty_100


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
        
    @staticmethod
    def fetch_sector_memberships_nifty_100():
        try:
            sector_memberships = compute_sector_memberships_nifty_100()
            if not sector_memberships:
                raise ValueError("No sector membership data found for Nifty 100")
            return sector_memberships
        except Exception as e:
            raise ValueError("Error fetching sector membership data for Nifty 100")

