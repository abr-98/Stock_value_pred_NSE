from application.helpers.data_fetchers_market import DataFetchersMarket

class DataFetchOrchestratorMarket:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_market_state(self) -> dict:

        return {
            "market_data": DataFetchersMarket.fetch_market_data(),
            "sector_memberships_nifty_100": DataFetchersMarket.fetch_sector_memberships_nifty_100()
        }
