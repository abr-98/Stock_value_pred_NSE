from application.helpers.data_fetcher_explaination import DataFetcherExplaination

class DataFetchersExplaination:
    """
    Pure world-state assembler.
    Does NOT compute indicators.
    """

    def build_explaination_state(self, symbol) -> dict:

        return { 
            "data": DataFetcherExplaination.fetch_symbol_value(symbol)
        }
