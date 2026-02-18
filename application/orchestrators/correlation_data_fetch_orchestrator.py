from application.helpers.data_fetcher_correlation import DataFetcherCorrelation

class DataFetchersCorrelation:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_market_state(self) -> dict:

        return { 
            "correlation_data": DataFetcherCorrelation.fetch_correlation_data()
        }
